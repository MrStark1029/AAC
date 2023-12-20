import numpy as np
import folium
import webbrowser
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import pickle

def sh(doru):
    if doru == 1:
        up = 0.26
        ij = 0.05
    else:
        up = 0.026
        ij = 0.005
    random_array = np.random.rand(10, 10) * 0.25
    plt.imshow(random_array, cmap='viridis', origin='lower', aspect='auto')
    cbar = plt.colorbar(label='Values')
    cbar.set_ticks(np.arange(0, up, ij))
    plt.xlabel('Crosstrack')
    plt.ylabel('Downtrack')
    plt.gca().add_patch(plt.Rectangle((-0.5, -0.5), random_array.shape[1], random_array.shape[0], color='white'))
    plt.xticks(np.arange(0, 1280, 200))
    plt.yticks(np.arange(1240, -1, -200))
    plt.show()



def dipl(LAT, LON):
    fig, ax = plt.subplots()
    im = ax.imshow(selected_event[j], cmap='viridis')
    if doru == 1:
        du = "Depth"
    elif doru == 2:
        du = "Uncertainty"
    titl ='Group' + str(ch) + ' ' + 'Band' + ' ' + du
    ax.set_title(titl)
    ax.set_xlabel('X-axis Label')
    ax.set_ylabel('Y-axis Label')
    plt.colorbar(im, ax=ax, label=('Band' + du))

    image_buffer = BytesIO()
    fig.savefig(image_buffer, format='png')
    image_buffer.seek(0)

    plt.close()
    image_base64 = base64.b64encode(image_buffer.read()).decode('utf-8')

    folium.CircleMarker(location=[LAT, LON], radius=3, color='green', fill=True, fill_color='green',fill_opacity=0.8,
                        popup=folium.Popup(f'<img src="data:image/png;base64,{image_base64}">', max_width=50)).add_to(
        m)

print("--------------------------------------------------------------------")
print()
print("Welcome to visualise EMIT data!")
print("Task @ AAC, VNIT")
print()
print("--------------------------------------------------------------------")
print()
print("Loading...")
print()

#loading the data
with open('data.pkl', 'rb') as f:
    loaded_data = pickle.load(f)
    g1bd, g2bd, g1bu, g2bu, lat, lon = loaded_data

# User inputs
ch = int(input("Select Band [1/2]: "))
doru = int(input("Select ----> 1] Depth OR 2] Uncertainty  = "))
sh(doru)
cr = float(input("Enter Crosstrack (X) value: "))
dr = float(input("Enter Downtrack (Y) value: "))
uppr = float(input("Enter the upper range: "))
lowr = float(input("Enter the lower range: "))

if ch == 1 and doru == 1:
    selected_event = g1bd
elif ch == 1 and doru == 2:
    selected_event = g1bu
elif ch == 2 and doru == 1:
    selected_event = g2bd
elif ch == 2 and doru == 2:
    selected_event = g2bu

lat_fin = []
lon_fin = []
for i in range(1, len(selected_event)):
    ele = (selected_event[i])[int(cr), int(dr)]
    if lowr <= ele <= uppr:
        lat_fin.append(lat[i])
        lon_fin.append(lon[i])

m = folium.Map(location=[0, 0], zoom_start=3    )
if len(lat_fin) >= 1:

    for j in range(0, len(lat_fin)):
        LAT = lat_fin[j][0]
        LON = lon_fin[j][0]
        dipl(LAT, LON)
    m.save('map_with_markers.html')
    webbrowser.open('map_with_markers.html', new=2)
else:
    print("Sorry No such location had those properties...Please Try Again !")
