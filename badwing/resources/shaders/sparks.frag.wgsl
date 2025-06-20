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
