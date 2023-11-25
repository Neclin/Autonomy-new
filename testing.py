import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

seed = 1
noise1 = PerlinNoise(octaves=1, seed=seed)
noise2 = PerlinNoise(octaves=1, seed=seed)
noise3 = PerlinNoise(octaves=12, seed=seed)
noise4 = PerlinNoise(octaves=24, seed=seed)

xpix, ypix = 500, 500
scale = 100
pic = []
for i in range(xpix):
    row = []
    for j in range(ypix):
        noise_val = (noise1([(i*scale)/xpix, (j*scale)/ypix])+1) / 2
        noise_val *= (noise2([(i*5)/(xpix), (j*5)/(ypix)])+1) / 2
        # noise_val += 0.25 * noise3([i/xpix, j/ypix])
        # noise_val += 0.125 * noise4([i/xpix, j/ypix])

        if noise_val > 0.3:
            row.append(noise_val)
        else:
            row.append(0)
    pic.append(row)

plt.imshow(pic, cmap='gray')
plt.show()
