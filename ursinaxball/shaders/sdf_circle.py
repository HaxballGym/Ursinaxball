from ursina import *

sdf_circle = Shader(
    language=Shader.GLSL,
    fragment="""
#version 430

uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;
in vec2 uv;
out vec4 color;

void main() {
    vec4 circle_col = texture(p3d_Texture0, uv) * p3d_ColorScale;
    vec4 bg_col = vec4(0.0);
    vec2 center = vec2(0.5);
    float smooth_cutoff = 0.01;
    float radius = 0.5;
    float sdf_factor = smoothstep(
      radius, 
      radius * (1.0 + smooth_cutoff), 
      length(uv - center)
    );
    color = mix(circle_col, bg_col, sdf_factor);
}
    """,
)

if __name__ == "__main__":
    app = Ursina()
    window.borderless = False
    window.exit_button.enabled = False

    e = Entity(
        model="quad",
        color=color.blue,
        shader=sdf_circle,
        scale=1,
        x=-2,
        y=1,
    )

    app.run()
