# Sử dụng image cơ sở Python
FROM python:3.8-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép tệp requirements.txt và cài đặt các gói
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Sao chép toàn bộ mã nguồn ứng dụng vào container
COPY . .

# Expose cổng mà ứng dụng chạy trên
EXPOSE 8000

# Command để chạy ứng dụng Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
