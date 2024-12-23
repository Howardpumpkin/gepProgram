from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# views.py

def home(request):
    return render(request, 'home.html')

def upload_file(request):
    if request.method == 'POST' and request.FILES['data_file']:
        data_file = request.FILES['data_file']
        df = pd.read_csv(data_file)

        # 假設數據包含 'latitude', 'longitude', 'gravity_anomaly', 'magnetic_anomaly'
        if {'latitude', 'longitude', 'gravity_anomaly', 'magnetic_anomaly'}.issubset(df.columns):
            # 繪製重力異常圖
            plt.figure(figsize=(8, 6))
            plt.scatter(df['longitude'], df['latitude'], c=df['gravity_anomaly'], cmap='viridis')
            plt.colorbar(label='Gravity Anomaly (mGal)')
            plt.title('Gravity Anomaly Map')
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            gravity_img = save_plot_to_base64()

            # 繪製磁力異常圖
            plt.figure(figsize=(8, 6))
            plt.scatter(df['longitude'], df['latitude'], c=df['magnetic_anomaly'], cmap='plasma')
            plt.colorbar(label='Magnetic Anomaly (nT)')
            plt.title('Magnetic Anomaly Map')
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            magnetic_img = save_plot_to_base64()

            return JsonResponse({
                'gravity_img': gravity_img,
                'magnetic_img': magnetic_img
            })
        else:
            return JsonResponse({'error': 'Invalid data format. Required columns: latitude, longitude, gravity_anomaly, magnetic_anomaly'})
    return JsonResponse({'error': 'No file uploaded'})


def save_plot_to_base64():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    encoded_img = base64.b64encode(image_png).decode('utf-8')
    plt.close()
    return f'data:image/png;base64,{encoded_img}'