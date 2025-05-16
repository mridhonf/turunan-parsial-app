import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Simbol ---
L, K = sp.symbols('L K')
C = 10*L**2 + 20*K**2 + 5*L*K 
# --- Turunan Parsial ---
dC_dL = sp.diff(C, L)
dC_dK = sp.diff(C, K)

# --- Judul Aplikasi ---
st.title("Aplikasi Analisis Biaya Tambahan Produksi Roti dengan Turunan Parsial")

# --- Keterangan ---
st.write("L = Tenaga Kerja")
st.write("K = Bahan Baku")
st.write("C = Total Biaya") 
st.write("1 Unit Roti = Rp 5000")
st.write("======================================================================================")
# --- Input User ---
f = sp.sympify(C)
fL = sp.diff(f, L)
fK = sp.diff(f, K)

st.latex(f"C(L, K) = {sp.latex(f)}")
st.latex(f"\\frac{{\\partial f}}{{\\partial L}} = {sp.latex(fL)}")
st.latex(f"\\frac{{\\partial f}}{{\\partial K}} = {sp.latex(fK)}")
st.write("======================================================================================")

L_val = st.number_input("Jumlah Tenaga Kerja (L)", value=0)
K_val = st.number_input("Jumlah Bahan Baku (K)", value=0)

# --- Evaluasi Turunan ---
dC_dL_val = dC_dL.subs({L: L_val, K: K_val})
dC_dK_val = dC_dK.subs({L: L_val, K: K_val})

st.write(f"### Fungsi Biaya: C(L, K) = 10L² + 20K² + 5LK")
st.write(f"Turunan Parsial terhadap L: ∂C/∂L = {dC_dL}")
st.write(f"Turunan Parsial terhadap K: ∂C/∂K = {dC_dK}")

st.write(f"### Hasil Perhitungan")
st.write(f" • Jika tenaga kerja(L) bertambah {L_val} unit, dengan bahan baku {K_val} unit (∂C/∂L) (L={L_val}, K={K_val}) Biaya Naik Sekitar ({dC_dL_val}) Unit")
hasil1 = dC_dL_val*5000
st.write(f"Hasil Biaya = {dC_dL_val} * 5000 = Rp {hasil1}")

st.write(f" • Jika bahan baku(K) bertambah {K_val} unit, dengan tenaga kerja {L_val} unit (∂C/∂K) (L={L_val}, K={K_val}) Biaya Naik Sekitar ({dC_dK_val}) Unit")
hasil2 = dC_dK_val*5000
st.write(f"Hasil Biaya = {dC_dK_val} * 5000 = Rp {hasil2}")

st.markdown("### Evaluasi di Titik:")

# --- Plot 3D ---
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Data grid
L_vals = np.linspace(0, 20, 50)
K_vals = np.linspace(0, 20, 50)
L_mesh, K_mesh = np.meshgrid(L_vals, K_vals)
C_func = sp.lambdify((L, K), C, 'numpy')
C_vals = C_func(L_mesh, K_mesh)

# Surface
ax.plot_surface(L_mesh, K_mesh, C_vals, cmap='viridis', alpha=0.7)

# Titik evaluasi dan bidang singgung
z0 = C_func(L_val, K_val)
grad_L = float(dC_dL_val)
grad_K = float(dC_dK_val)
Z_tangent = z0 + grad_L * (L_mesh - L_val) + grad_K * (K_mesh - K_val)
ax.plot_surface(L_mesh, K_mesh, Z_tangent, color='red', alpha=0.3)

ax.scatter(L_val, K_val, z0, color='black', s=50)
ax.set_xlabel('Tenaga Kerja (L)')
ax.set_ylabel('Bahan Baku (K)')
ax.set_zlabel('Biaya C(L,K)')
ax.set_title('Grafik Fungsi Biaya dan Bidang Singgung')
st.pyplot(fig)
