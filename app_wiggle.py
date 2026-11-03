
"""
app_wiggle.py — Fallback Wiggle-only — No live APIs — For offline demo
Same as live_ac_sor_70k_wiggle.py but Streamlit
"""

import streamlit as st, math
import plotly.graph_objects as go

st.set_page_config(page_title="DataFidelis — AC $70k Wiggle — Fallback", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth=False
if not st.session_state.auth:
    u=st.text_input("Username"); p=st.text_input("Password",type="password")
    if st.button("Login"):
        if u=="jefe" and p=="DataFidelis2026!":
            st.session_state.auth=True; st.rerun()
    st.stop()

def sinh_safe(x): return math.sinh(max(-20,min(20,x)))
def ac_traj(X,T,N,lam,sigma_daily,eta):
    sigma_sec=sigma_daily/math.sqrt(86400)
    if eta==0 or lam==0: return [X*(1-k/N) for k in range(N+1)],0
    kappa=math.sqrt(lam*sigma_sec*sigma_sec/eta)
    return [X*sinh_safe(kappa*(T-T*k/N))/sinh_safe(kappa*T) if sinh_safe(kappa*T)!=0 else X*(1-k/N) for k in range(N+1)],kappa

st.title("WIGGLE IT — BTC $70k — Fallback — No Live APIs — DataFidelis")
price=st.sidebar.slider("BTC Price",65000,85000,70000,100)
lam=st.sidebar.slider("Lambda",0.01,10.0,10.0,0.01)
sigma_pct=st.sidebar.slider("Sigma %",1.0,12.0,12.0,0.1)
X=st.sidebar.slider("X BTC",1,100,51)
T=st.sidebar.slider("T s",60,3600,2160)

sigma_daily=sigma_pct/100; eta=0.1; N=10
ac_list,kappa=ac_traj(X,T,N,lam,sigma_daily,eta)
front=(X-ac_list[2])/X*100

crash_factor=(80000-price)/80000; sigma_factor=(sigma_pct-3.46)/10
cb_mid=price-300-crash_factor*2000-sigma_factor*1000
by_mid=price+500+crash_factor*3000+sigma_factor*1500
orca_mid=price-100-crash_factor*500
cb_eff=(cb_mid+1)*1.0008; by_eff=(by_mid+1)*1.0005; orca_eff=(orca_mid+1)*0.9996
save_usd=max(cb_eff,by_eff,orca_eff)-min(cb_eff,by_eff,orca_eff)
save_bps=save_usd/min(cb_eff,by_eff,orca_eff)*10000

st.metric("Save", f"${save_usd:,.0f} ({save_bps:.0f} bps)")
times=[i*T/N for i in range(N+1)]
fig=go.Figure()
fig.add_trace(go.Scatter(x=times,y=ac_list,mode='lines+markers',name=f'AC {front:.0f}%'))
st.plotly_chart(fig)
