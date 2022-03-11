#version 430

#define PI 3.1415926535
out vec4 fragColor;
uniform vec2 resolution;
uniform float time;
uniform bool is;
uniform vec3 color_1;
uniform vec3 color_2;
uniform vec3 color_3;
uniform float speed;
uniform float part_count;

mat2 scale(vec2 scale){
    return mat2(scale.x,0.0,0.0,scale.y);
}
vec2 rotate(vec2 v, float a) {
	float s = sin(a);
	float c = cos(a);
	mat2 m = mat2(c, -s, s, c);
	return m * v;
}

vec2 hash12(float t){
    float x = fract(sin(sin(t*3453.329)));
    float y = fract(sin((t+x))*8532.732);
    return vec2(x,y);
}
void main ( void ){
    vec2 uv = (gl_FragCoord.xy-0.5*resolution.xy)/resolution.y;
    vec3 col = vec3(0.0);
    col+=0.01/length(uv+(vec2(sin(time*PI*speed),cos(time*PI*PI*speed)*0.2))/2.);
    for(int i =0; i<part_count; i++){
        float radius = 0.5;
        float rad = radians(360.0/part_count)*float(i);
        //rad+=vec2(2.*PI*sin(time),2.*PI*cos(time)).x+time;//backandforth
        rad+=time*2.;
        float scale = 2/(3-cos(2*rad));
        if(is)
            col+=vec3(0.1*0.1/length(uv + vec2(radius*cos(rad)*scale,scale*radius*sin(rad*2)/2)));
    }
    vec3 c1 = color_1;
    vec3 c2 = color_2;
    col*=mix(c1,c2,uv.x);
    col = pow(col,vec3(1.69));
    fragColor = vec4(col,1.0);
}