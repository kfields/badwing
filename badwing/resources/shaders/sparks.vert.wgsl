{% include '_camera.wgsl' %}
{% include '_model.wgsl' %}
{% include '_particle.vert.wgsl' %}

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
    output.position = camera.projection * camera.view * model.transform * vec4<f32>(vert_pos.x, vert_pos.y, 0.0, 1.0);
    output.color = particles[instanceIndex].color;
    output.age = particles[instanceIndex].age;
    output.lifespan = particles[instanceIndex].lifespan;
    return output;
}
