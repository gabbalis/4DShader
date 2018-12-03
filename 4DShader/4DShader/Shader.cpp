#define fl float
#define ff const fl
//ff minY=0.;//minimum height.

#define TAU 6.28318530718

//The edges of the image are pointing diagonally, because light comes from them diagonally.
//Similarly, the direction the entire screen is pointing is more and more Z oriented towards
//the left and rightmost images.
//these walls are 2d planes, but in 3d sight they are percieved as 3D shapes.
int getRoot(ivec2 resolution) {
    int root = 1;
    int x = 1;
    while (true)
    {
      x = x + 1;
      if (x*x*x > resolution.x * resolution.y)
      {
        return root;
      }
      if ((int(resolution.x)/x * int(resolution.y)/x) < x)
      {
        return root;
      }
      root = x;
    }
}

// This function makes the x dimention left right, Y up down, and Z previous/next square.
ivec3 getCubeXYZ(int numwide, int numtall, int root, ivec2 pxcoords, int border_px){
    ivec3 none = ivec3(999,999,999);
    int bordered_root = border_px + root;
    int xrem = pxcoords.x % bordered_root;
    int yrem = pxcoords.y % bordered_root;
    if (xrem > root || yrem > root)
    {
        return none;
    }
    if (pxcoords.x >= numwide * bordered_root)
    {
        return none;
    }
    if (pxcoords.y >= numtall * bordered_root)
    {
        return none;
    }
    ivec2 DepthCoords = ivec2(pxcoords.x/bordered_root, pxcoords.y/bordered_root);
    ivec3 coords = ivec3 (xrem, yrem, DepthCoords.y * numwide + DepthCoords.x);
    return coords;
}


vec3 checkScene(vec4 point){

    //Hypersphere
    if (pow(point.w - 2.0, 2.0) + pow(point.x, 2.0) + pow(point.y,2.0) + pow(point.z,2.0) <= .5)
    {   //Blue
        return vec3(0.0, 0.0, 1.0);
    }

    //Hypercylendar
    if (pow(point.w-2.0, 2.0) + pow(point.x,2.0) + pow(point.y,2.0) <= 0.2)
    {   //green
        return vec3(.3, 1.0, 0.0);
    }

    //HyperWalls
    if (point.w > 5.0 && point.w < 5.3){//Dark Red
        return vec3(0.5, 0.0, 0.0);}
    if (point.w < -5.0 && point.w > -5.3){//Dark Green
        return vec3(0.0, 0.5, 0.0);}
    if (point.x > 5.0 && point.x < 5.3){//Dark Blue
        return vec3(0.0, 0.0, 0.5);}
    if (point.x < -5.0 && point.x > -5.3){//Dark Yellow
        return vec3(0.5, 0.5, 0.0);}
    if (point.y > 5.0 && point.y < 5.3){//Dark Purple
        return vec3(0.5, 0.0, 0.5);}
    if (point.y < -5.0 && point.y > -5.3){//Dark Cyan?
        return vec3(0.0, 0.5, 0.5);}
    if (point.z > 5.0 && point.z < 5.3){//Gray
        return vec3(0.5, 0.5, 0.5);}
    if (point.z < -5.0 && point.z > -5.3){//Grayish
        return vec3(0.2, 0.1, 0.2);}

    return vec3 (0.0, 0.0, 0.0);
}


vec3 rayTrace(vec4 cube_px_coords, vec4 camera_coords){
    float traced_dist = 0.0;
    vec3 color = vec3(0, 0, 0);
    float trace_dist = 0.05;
    vec4 dir_vector = cube_px_coords + camera_coords;
    vec4 unit_vector = dir_vector/pow(length(dir_vector),2.); //angle between camera and cube
    vec4 point = cube_px_coords;
    while (traced_dist < 20.0 && color == vec3(0, 0, 0)){
        color = checkScene(point);
        traced_dist = traced_dist + trace_dist;
        point = point + trace_dist * unit_vector;
    }
    //illuminate nearby things
    float illumination = 1.0-pow(traced_dist, 1.2)/10.0;
    illumination = max(illumination, -0.1);
    return color*(1.0-illumination) + vec3(illumination);
}

mat4 getRotMatrix(vec3 rotation){
    float aaa = rotation.x, bbb = rotation.y, ccc = rotation.z;
    float c1 = cos(aaa), s1 = sin(aaa),
          c2 = cos(bbb), s2 = sin(bbb),
          c3 = cos(ccc), s3 = sin(ccc);
    mat4 B;
    B = mat4(c2,  s2*s3,   0, -s2*c3,
                          0,  c1*c3, -s1,  c1*s3,
                          0,  c3*s1,  c1,  s1*s3,
                         s2, -c2*s3,   0,  c2*c3);
    return B;
}

vec4 getVariable(int varnum){
    fl x = fl(varnum) + 0.5;
    return texture(iChannel3,vec2(x,.5)/iResolution.xy,-10.);}

void mainImage( out vec4 fragColor, in vec2 fragCoord ){

    vec4 LocOffset = getVariable(0);
    vec3 RotOffset = getVariable(1).wxy*TAU;

    // Rotation Matrix to apply to 4D objects


    int border_px = 2; //issue: Border currently eats the image instead of squishing it.
    ivec2 res = ivec2 (iResolution);
    int root = getRoot(res) - border_px;
    int numwide = (res.x/(root+border_px));
    int numtall = (res.y/(root+border_px));
    ivec2 pxcoords = ivec2(fragCoord.x , iResolution.y - fragCoord.y);

    ivec3 cubeCoords = getCubeXYZ(numwide, numtall, root, pxcoords, border_px);
    if (cubeCoords == ivec3(999,999,999))
    {
        fragColor = vec4(0.0,0.0,0.0,1.0);
        return;
    }
    vec4 normalizedCubeCoords = vec4(0.0, (vec3(cubeCoords)/float(root + border_px))*2.0-1.0);
    // Now the camera is on w axis pointing at this cube. a unit away.
    mat4 rotMatrix = getRotMatrix(RotOffset);
    vec4 camera_coords = vec4((-0.2, 0.0, 0.0, 0.0)*rotMatrix) + LocOffset;
    normalizedCubeCoords = vec4(normalizedCubeCoords*rotMatrix) + LocOffset;

    vec3 col = rayTrace(normalizedCubeCoords, camera_coords);
    fragColor = vec4(col,1.0);
}
