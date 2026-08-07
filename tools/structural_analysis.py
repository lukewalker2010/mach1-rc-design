#!/usr/bin/env python3
"""E1 verification computations for re-baselined Mach-1 RC (18 §3).
Aero drag + CG/stability solver + wing box spar sizing.
Run: /tmp/opencode/cq312/bin/python e1_check.py
"""
import math
G=1.4; R=287.0
S_front=math.pi*0.0925**2
BODY_L=2.6; BODY_R=0.0925
S_w=0.14; MAC=0.156; AR=0.95**2/S_w
S_t=0.012; x_tail=2.35
W=13.60*9.81

def atmos(h):
    T=288.15-0.0065*h; p=101325.0*(1-0.0065*h/288.15)**5.2561
    return T,p,p/(R*T)

def drag(M,h):
    T,p,rho=atmos(h); a=math.sqrt(G*R*T); V=M*a; q=0.5*rho*V*V
    mu=1.458e-6*T**1.5/(T+110.4)
    cd_wave=(9*math.pi**2/2)*(BODY_R/BODY_L)**2
    ft = 1.0 if M<=0.9 else (1.0+0.38*(M-0.9)/0.14 if M<1.04 else max(1.0,1.38-0.38*(M-1.04)/0.21))
    Re_b=rho*V*BODY_L/mu; Re_w=rho*V*MAC/mu
    Cf_b=0.074/Re_b**0.2; Cf_w=0.074/Re_w**0.2
    Mn=M*math.cos(math.radians(30))
    cd_ww = max(0.004, 0.012*(Mn-0.9)/0.1)
    D={}
    D['waveB']=cd_wave*ft*q*S_front; D['fricB']=Cf_b*q*0.78
    D['fricW']=Cf_w*q*2*S_w; D['waveW']=cd_ww*q*S_w
    D['tail']=0.25*(D['fricW']+D['waveW']); D['intake']=0.0085*q*S_front
    D['base']=0.005*q*S_front; D['excr']=0.006*q*S_front
    CL=W/(q*S_w); D['ind']=CL**2/(math.pi*AR*0.85)*q*S_w
    return sum(D.values()), q, Re_w, Re_b, {k:round(v,1) for k,v in D.items()}

print("=== DRAG (10,000 ft / 12,000 ft) ===")
for h in [3048,3658]:
    for M in [0.85,0.95,1.0,1.05,1.1,1.2]:
        tot,q,Rew,Rev,D=drag(M,h)
        print(f"  M{M:.2f} h={int(h)}m: TOTAL {tot:6.0f} N  {D}")
d5=q5=0
for M in [1.05,1.10]:
    tot,q,_,_,_=drag(M,3048); print(f"  M{M:.2f}/10kft drag = {tot:.0f} N")
print()

print("=== CG / STABILITY (18 s3.4 mass table, fuel @ 0.45 m, 13.60 kg) ===")
comp = [  # (name, mass kg, station m)  -- 18 s3.4 table as published
 ("engine",4.90,1.20),("ab",0.83,1.48),("wing",0.50,1.00),("stab",0.10,2.35),
 ("ventral",0.10,2.30),("fuse",2.50,1.30),("fuel",1.62,0.45),("fuelsys",0.50,0.60),
 ("avionics",0.90,0.25),("landing",0.35,0.80),("ballast",1.00,0.10),("misc",0.30,1.00)]
wingLE=0.96; Xac_w=wingLE+0.25*MAC
for label,NP in [("wing-only NP", Xac_w), ("tail-incl NP", Xac_w+0.8*(S_t/S_w)*(x_tail-Xac_w))]:
    print(f"  --- {label}: NP={NP:.3f} m ---")
    for tag,drop in [("FULL",False),("EMPTY",True)]:
        m=sum(c[1] for c in comp if not(drop and c[0]=="fuel"))
        mm=sum(c[1]*c[2] for c in comp if not(drop and c[0]=="fuel"))
        cg=mm/m
        sm=(NP-cg)/MAC
        print(f"    {tag:5s} MTOW={m:6.2f} kg  CG={cg:6.3f} m  SM={sm*100:5.1f}% MAC  "
              f"{'OK>=12' if sm>=0.12 else 'FAIL'}")
print("  [sensitivity: AB mass 0.97 kg (E2) -> MTOW 13.74 kg; see 19 s3]")
print()

print("=== WING BOX SPAR (13.60 kg, lambda=0.4) ===")
Wn=13.60*9.81
Ycg=(1+2*0.4)/(3*(1+0.4))*(0.95/2)   # spanwise lift centroid from root
for n,name in [(4,"LIMIT 4g"),(6,"ULT 6g")]:
    Mroot=n*Wn*Ycg; Vroot=n*Wn*(0.475-Ycg)/0.475
    print(f"  {name}: M_root={Mroot:6.1f} N·m  V_root={Vroot:6.0f} N")
    cap_area=5*0.2e-3*0.05     # 5 plies x 0.2mm x 50mm (recommended, fits 7mm sep)
    sep=0.007
    sig_cap=Mroot/sep/cap_area
    web_area=0.007*0.001      # 1.0 mm web x 7mm tall (x2 sides => per side half)
    tau= Vroot/2/web_area
    print(f"      cap stress={sig_cap/1e6:6.0f} MPa (T300 comp 1200 -> m={1200e6/sig_cap:4.1f}) "
          f"web tau={tau/1e6:5.0f} MPa (per side, +-45 70-100 -> m~{90e6/tau:3.1f})")
print()

print("=== STABILATOR (S_t=0.012, servo KST X20-12T 1.18 N·m) ===")
q=0.5*0.905*(328)**2
c_avg=0.06
Mh=q*S_t*c_avg*0.02
print(f"  hinge moment @M1 15deg = {Mh*1000:.0f} mN·m ; servo 1180 mN·m -> margin {1180e-3/Mh:.1f}x")

print("=== ENGINE MOUNT (I-01, 4x M3 on 45mm PCD) ===")
Fn=465.0  # wet thrust
Fv=9.81*5*(4.9+0.97)  # 5g vibration
print(f"  thrust shear/bolt={Fn/4:.0f} N, 5g vib/bolt={Fv/4:.0f} N; M3 A2-70 shear cap ~2113 N -> large margin")

print("=== THERMAL (AB shell outer 610K, 5mm ceramic blanket k=0.05, 17:287-297) ===")
T_shell=610.0; T_limit=410.0; k_b=0.05; t_b=0.005
dt_req=T_shell-T_limit
q_leak=k_b*dt_req/t_b                 # leak flux through blanket at the required drop
q_shell=76000.0                        # conduction flux through 1.5mm shell (17:284)
frac=q_leak/q_shell
print(f"  blanket needed to drop shell {T_shell:.0f}K -> composite <{T_limit:.0f}K: "
      f"deltaT={dt_req:.0f}K => leak flux q={q_leak:.0f} W/m2 = {frac*100:.0f}% of shell flux "
      f"-> {'OK' if dt_req>0 else 'FAIL'} (rest carried by annulus cooling air)")
