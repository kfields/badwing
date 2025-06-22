from loguru import logger

from crunge.core import klass
from crunge import wgpu

from crunge.engine.d2.bindings_2d import EmitterBindGroupLayout
from crunge.engine.loader.shader_loader import ShaderLoader
from crunge.engine.d2.render_pipeline_2d import RenderPipeline2D

from ...badwing_program import BadwingProgram

class SparksRenderPipeline(RenderPipeline2D):
    @property
    def model_bind_group_layout(self):
        return EmitterBindGroupLayout()


@klass.singleton
class SparksProgram(BadwingProgram):
    def __init__(self):
        super().__init__()
        self.cs_module = ShaderLoader(self.template_env, self.template_dict).load(
            "sparks.comp.wgsl"
        )
        self.vs_module = ShaderLoader(self.template_env, self.template_dict).load(
            "sparks.vert.wgsl"
        )
        self.fs_module = ShaderLoader(self.template_env, self.template_dict).load(
            "sparks.frag.wgsl"
        )

        self.create_render_pipeline()
        self.create_compute_bind_group_layouts()
        self.create_compute_pipeline()

    def create_render_pipeline(self):
        self.render_pipeline = SparksRenderPipeline(
            vertex_shader_module=self.vs_module, fragment_shader_module=self.fs_module
        ).create()

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
            compute=wgpu.ComputeState(
                module=self.cs_module,
                entry_point="cs_main",
            ),
        )
        self.compute_pipeline = self.device.create_compute_pipeline(compute_pl_desc)
        logger.debug(self.compute_pipeline)
