from ctypes import sizeof
import random

from loguru import logger
import glm

from crunge.core import as_capsule
from crunge.core import klass
from crunge import wgpu
import crunge.wgpu.utils as utils

from crunge.engine import Renderer

from crunge.engine.program import Program
from crunge.engine.d2.vu_2d import Vu2D
from crunge.engine.uniforms import cast_matrix4, cast_vec4
from crunge.engine.d2.uniforms_2d import (
    ModelUniform,
)

from .uniforms import Particle, Vec2, Vec4

PARTICLE_COUNT = 32
PARTICLE_SIZE = glm.vec2(6, 6)
PARTICLE_VELOCITY = 0.5
PARTICLE_LIFESPAN = 50.0

cs_code = """
struct Particle {
    position: vec2<f32>,
    velocity: vec2<f32>,
    color: vec4<f32>,
    age: f32,
    lifespan: f32,
}
@group(0) @binding(0) var<storage, read_write> particles: array<Particle>;

@compute @workgroup_size(64) // Adjust workgroup size based on your needs
fn cs_main(@builtin(global_invocation_id) global_id : vec3<u32>) {
    let id = global_id.x;
    if (particles[id].age < particles[id].lifespan) {
        particles[id].position += particles[id].velocity;
        particles[id].age += 1.0;
        // Update other properties as needed
    } else {
        // Reset or hide the particle
    }
}
"""

vs_code = """
struct Camera {
    projection : mat4x4<f32>,
    view : mat4x4<f32>,
    position: vec3<f32>,
}
@group(0) @binding(0) var<uniform> camera : Camera;

@group(1) @binding(0) var<uniform> model : mat4x4<f32>;

struct Particle {
    position: vec2<f32>,
    velocity: vec2<f32>,
    color: vec4<f32>,
    age: f32,
    lifespan: f32,
}
@group(1) @binding(1)  var<storage, read> particles: array<Particle>;

struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) color: vec4<f32>,
    @location(1) age: f32,
    @location(2) lifespan: f32,
}

@vertex
fn vs_main(@builtin(vertex_index) vertexIndex: u32, @builtin(instance_index) instanceIndex: u32) -> VertexOutput {
    var output: VertexOutput;

    let x = f32((vertexIndex & 1u) << 1) - 1.0; // Generates -1.0 or 1.0
    let y = f32((vertexIndex & 2u) >> 1) * 2.0 - 1.0; // Generates -1.0 or 1.0

    let pos = vec2<f32>(x * 0.5, y * 0.5); // Scale quad by 0.5

    let vert_pos = pos + particles[instanceIndex].position;
    output.position = camera.projection * camera.view * model * vec4<f32>(vert_pos.x, vert_pos.y, 0.0, 1.0);
    output.color = particles[instanceIndex].color;
    output.age = particles[instanceIndex].age;
    output.lifespan = particles[instanceIndex].lifespan;
    return output;
}
"""

fs_code = """
struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) color: vec4<f32>,
    @location(1) age: f32,
    @location(2) lifespan: f32,
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
    let fadeFactor: f32 = 1.0 - (in.age / in.lifespan);
    // Optionally clamp fadeFactor to avoid negative values
    // fadeFactor = max(fadeFactor, 0.0);

    let outColor = vec4<f32>(in.color.rgb, in.color.a * fadeFactor);
    return outColor;
}
"""


@klass.singleton
class SparksProgram(Program):
    def __init__(self):
        super().__init__()
        logger.debug("ExplosionProgram.__init__")
        self.cs_module = self.gfx.create_shader_module(cs_code)
        self.vs_module = self.gfx.create_shader_module(vs_code)
        self.fs_module = self.gfx.create_shader_module(fs_code)

        self.create_render_bind_group_layouts()
        self.create_render_pipeline()
        self.create_compute_bind_group_layouts()
        self.create_compute_pipeline()

    def create_render_bind_group_layouts(self):
        logger.debug("create_render_bind_group_layouts")
        camera_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        camera_bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=camera_bgl_entries)
        camera_bgl = self.device.create_bind_group_layout(camera_bgl_desc)
        logger.debug(f"camera_bgl: {camera_bgl}")

        # Render Bind Group Layout Entries
        render_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.UNIFORM,
                    min_binding_size=0,
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=1,
                visibility=wgpu.ShaderStage.COMPUTE | wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.READ_ONLY_STORAGE,
                    min_binding_size=0,
                ),
            ),
        ]

        # Render Bind Group Layout
        render_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            label="Render Bind Group Layout",
            entries=render_bgl_entries,
        )
        render_bgl = self.device.create_bind_group_layout(render_bgl_desc)

        self.render_bind_group_layouts = [camera_bgl, render_bgl]

    def create_render_pipeline(self):
        blend_state = wgpu.BlendState(
            alpha=wgpu.BlendComponent(
                operation=wgpu.BlendOperation.ADD,
                src_factor=wgpu.BlendFactor.ONE,
                dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
            ),
            color=wgpu.BlendComponent(
                operation=wgpu.BlendOperation.ADD,
                src_factor=wgpu.BlendFactor.SRC_ALPHA,
                dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
            ),
        )

        color_targets = [
            wgpu.ColorTargetState(
                format=wgpu.TextureFormat.BGRA8_UNORM,
                blend=blend_state,
                write_mask=wgpu.ColorWriteMask.ALL,
            )
        ]

        fragmentState = wgpu.FragmentState(
            module=self.fs_module,
            entry_point="fs_main",
            targets=color_targets,
        )

        vertex_state = wgpu.VertexState(
            module=self.vs_module,
            entry_point="vs_main",
        )

        primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_STRIP)

        depth_stencil_state = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            depth_write_enabled=False,
        )

        # Render Pipeline Layout
        render_pll_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layouts=self.render_bind_group_layouts
        )

        render_pl_desc = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(render_pll_desc),
            vertex=vertex_state,
            primitive=primitive,
            fragment=fragmentState,
            depth_stencil=depth_stencil_state,
        )

        logger.debug(render_pl_desc)
        self.render_pipeline = self.device.create_render_pipeline(render_pl_desc)
        logger.debug(self.render_pipeline)

    def create_compute_bind_group_layouts(self):
        # Compute Bind Group Layout Entries
        compute_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.COMPUTE,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.STORAGE,
                    min_binding_size=0,
                ),
            ),
        ]

        # Compute Bind Group Layout
        compute_bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=compute_bgl_entries)
        compute_bgl = self.device.create_bind_group_layout(compute_bgl_desc)

        self.compute_bind_group_layouts = [compute_bgl]

    def create_compute_pipeline(self):

        # Compute Pipeline Layout
        compute_pll_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layouts=self.compute_bind_group_layouts
        )

        compute_pl_desc = wgpu.ComputePipelineDescriptor(
            label="Main Compute Pipeline",
            layout=self.device.create_pipeline_layout(compute_pll_desc),
            # compute=wgpu.ProgrammableStageDescriptor(
            compute=wgpu.ComputeState(
                module=self.cs_module,
                entry_point="cs_main",
            ),
        )
        self.compute_pipeline = self.device.create_compute_pipeline(compute_pl_desc)
        logger.debug(self.compute_pipeline)


class SparksVu(Vu2D):
    model_uniform_buffer: wgpu.Buffer = None
    model_uniform_buffer_size: int = 0

    particles_buffer: wgpu.Buffer = None

    def __init__(self, color: glm.vec4 = glm.vec4(0.0, 0.0, 1.0, 1.0)):
        super().__init__()
        self.color = color
        self.program = SparksProgram()

        self.num_particles = PARTICLE_COUNT
        self.create_particles()
        self.create_buffers()
        self.create_bindgroups()

    @property
    def size(self):
        # return glm.vec2(10, 10)
        return PARTICLE_SIZE

    def create_particles(self):
        logger.debug("create_particles")
        self.particles = (Particle * self.num_particles)()
        for i in range(0, self.num_particles):
            self.particles[i].position = Vec2(0.0, 0.0)
            self.particles[i].velocity = Vec2(
                random.uniform(-PARTICLE_VELOCITY, PARTICLE_VELOCITY),
                random.uniform(-PARTICLE_VELOCITY, PARTICLE_VELOCITY),
            )
            self.particles[i].color = cast_vec4(self.color)
            self.particles[i].age = 0.0
            self.particles[i].lifespan = PARTICLE_LIFESPAN

    def create_buffers(self):
        logger.debug("create_buffers")
        self.particles_buffer = utils.create_buffer_from_ctypes_array(
            self.device, "PARTICLES", self.particles, wgpu.BufferUsage.STORAGE
        )
        # Uniform Buffers
        self.model_uniform_buffer_size = sizeof(ModelUniform)
        self.model_uniform_buffer = self.gfx.create_buffer(
            "Model Buffer",
            self.model_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bindgroups(self):
        compute_bindgroup_entries = [
            wgpu.BindGroupEntry(binding=0, buffer=self.particles_buffer),
        ]

        compute_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Compute bind group",
            layout=self.program.compute_pipeline.get_bind_group_layout(0),
            entries=compute_bindgroup_entries,
        )

        self.compute_bind_group = self.device.create_bind_group(compute_bind_group_desc)
        logger.debug(self.compute_bind_group)

        render_bindgroup_entries = [
            wgpu.BindGroupEntry(
                binding=0,
                buffer=self.model_uniform_buffer,
                size=self.model_uniform_buffer_size,
            ),
            wgpu.BindGroupEntry(binding=1, buffer=self.particles_buffer),
        ]

        render_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Render bind group",
            layout=self.program.render_pipeline.get_bind_group_layout(1),
            entries=render_bindgroup_entries,
        )

        self.render_bind_group = self.device.create_bind_group(render_bind_group_desc)

    def _draw(self):
        renderer = Renderer.get_current()

        model_uniform = ModelUniform()
        model_uniform.transform.data = cast_matrix4(self.transform)

        renderer.device.queue.write_buffer(self.model_uniform_buffer, 0, model_uniform)

        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.render_pipeline)
        pass_enc.set_bind_group(1, self.render_bind_group)
        pass_enc.draw(4, self.num_particles)

    def update(self, delta_time: float):
        # logger.debug("sparks update")
        compute_pass = wgpu.ComputePassDescriptor(
            label="Main Compute Pass",
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()

        compute_pass = encoder.begin_compute_pass(compute_pass)
        compute_pass.set_pipeline(self.program.compute_pipeline)
        compute_pass.set_bind_group(0, self.compute_bind_group)
        compute_pass.dispatch_workgroups(1)
        compute_pass.end()
        command_buffer = encoder.finish()

        self.queue.submit([command_buffer])
