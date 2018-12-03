//WASD-Movement
//Ben Quantock 2016
//License Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
//shortened&modified by ollj
#define fl float
#define ff const fl
ff minY=0.;//minimum height.
ff yMul=-1.;//negate to invert y-axis in controls
ff acc =.001;//acceleration
ff fri =.95;//friction
ff racc =.0005;//rotational acceleration
ff rfri =.95;//rotational 'friction'

//if both are disabled, it uses both (zq=wa)+sd+f+space
//#define wasd
//#define zqsd

#define cf 256.;
#define cfc cf ff
ff Key_left=37.5/cfc Key_up=38.5/cfc Key_right=39.5/cfc Key_down=40.5/cfc Key_Space=32.5/cfc
Key_0=48.5/cfc Key_1=49.5/cfc Key_2=50.5/cfc Key_3=51.5/cfc Key_4=52.5/cfc Key_5=53.5/cfc Key_6=54.5/cfc Key_7=55.5/cfc Key_8=56.5/cfc Key_9=57.5/cfc
Key_A=65.5/cfc Key_B=66.5/cfc Key_C=67.5/cfc Key_D=68.5/cfc Key_E=69.5/cfc Key_F=70.5/cfc Key_G=71.5/cfc Key_H=72.5/cfc Key_I=73.5/cfc Key_J=74.5/cfc Key_K=75.5/cfc Key_L=76.5/cfc Key_M=77.5/cfc Key_N=78.5/cfc Key_O=79.5/cfc Key_P=80.5/cfc Key_Q=81.5/cfc Key_R=82.5/cfc Key_S=83.5/cfc Key_T=84.5/cfc Key_U=85.5/cfc Key_V=86.5/cfc Key_W=87.5/cfc Key_X=88.5/cfc Key_Y=89.5/cfc Key_Z=90.5/cf
fl rkInternal(fl k,fl t){return texture(iChannel3,vec2(k,t)).x;}
fl rk      (fl k){return rkInternal(k,.25);}
fl rkToggle(fl k){return rkInternal(k,.75);}
vec4 chan0(fl x){return texture(iChannel1,vec2(x,.5)/iResolution.xy,-100.);}

//Don't i need 4 or 6 to represent it? why 3? What does this matrix dooo
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


void mainImage(out vec4 r, in vec2 i){r=vec4(0.,0.,0.,1.);if(int(i.y)==0){
 if(int(i.x)==0){//x=0 stores CameraPosition.wxyz; .w stores if the camera is flying: if(camPos.w>.0) is flying, no gravity|jumping
  vec4 camPos=chan0(.5);
  vec4 camVel=chan0(3.5);
  r=camPos+camVel;


 }else if(int(i.x)<2){//x=1. stores [cameraRot=0] in radians; .w stores iMouse.z, if mouse was held down at the last frame.
  vec4 rotVel=chan0(2.5);
  vec4 rotPos=chan0(1.5);
  r=rotPos+rotVel;

 }else if(int(i.x)==2){//x=2 stores [rotVel=rv] for acceleration and friction.
     vec4 vr=chan0(2.5);//rvel
     vec4 RotationMod = vec4(0.);
     RotationMod.w += rk(Key_U)-rk(Key_J);
     RotationMod.x += rk(Key_I)-rk(Key_K);
     RotationMod.y += rk(Key_O)-rk(Key_L);
     vr += RotationMod *racc;
     vr*=rfri;
     r=vr;
 }
  else if(int(i.x)==3){//x=3. stores [cameraVel=v] for acceleration and friction.
  vec4 p=chan0(.5);//pos
  vec4 v=chan0(3.5);//vel
  vec3 o=chan0(1.5).wxy*6.28318530718;//rot

  // some sort of rotation?
  // vec3 f=acc*vec3(0,0,1);vec3 l=f.zxx;
  //fl s;
  //fl c;
  //s=sin(o.x); c=cos(o.x);
  //f.zy=f.zy*c+s*vec2(1,-1)*f.yz;
  //l.zy=l.zy*c+s*vec2(1,-1)*l.yz;

  //s=sin(o.y); c=cos(o.y);
  //f.xz=f.xz*c+s*vec2(1,-1)*f.zx;
  //l.xz=l.xz*c+s*vec2(1,-1)*l.zx;

  vec4 MovementMod = vec4(0.);
  //Movement: W(ws)Z(ed)X(af)Y(TG)
  MovementMod.w += rk(Key_W)-rk(Key_S);
  MovementMod.y += rk(Key_E)-rk(Key_D);
  MovementMod.x += rk(Key_A)-rk(Key_F);
  MovementMod.z += rk(Key_T)-rk(Key_G);

  mat4 rotMatrix = getRotMatrix(o);
  v += MovementMod*rotMatrix*acc;
  //v.wxyz+=vec4((rk(Key_W)-rk(Key_S))*f, 0.);
  //v.wxyz+=vec4((rk(Key_D)-rk(Key_A))*l, 0.);


  v*=fri;
  r=v;}}}
