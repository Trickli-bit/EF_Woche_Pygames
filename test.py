import numpy as np
import matplotlib.pyplot as plt

# Beispielpunkte für Glasprofil (y, x)
points_y = np.array([0, 1, 3, 4, 7, 10])
points_x = np.array([0.2, 0.5, 0.2, 0.3, 1.5, 0.2])

# Polynomfit (Grad 5, da 6 Punkte)
coeffs = np.polyfit(points_y, points_x, 5)
poly = np.poly1d(coeffs)

# Auswertung
y_vals = np.linspace(0, 10, 400)
x_vals = poly(y_vals)

# Plot
plt.plot(x_vals, y_vals, 'b', label="Polynomprofil")
plt.plot(-x_vals, y_vals, 'b')
plt.scatter(points_x, points_y, color="red", label="Stützpunkte")
plt.scatter(-points_x, points_y, color="red")
plt.gca().set_aspect('equal')
plt.legend()
plt.title("Weinglas als Polynomprofil")
plt.show()

print("Polynomkoeffizienten (x in Abhängigkeit von y):")
print(poly)