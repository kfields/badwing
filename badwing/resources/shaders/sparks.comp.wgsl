{% include '_particle.comp.wgsl' %}

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
