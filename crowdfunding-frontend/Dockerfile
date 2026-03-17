FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Đặt biến môi trường API_URL để Angular connect backend
ENV API_URL=http://django_backend:8080

EXPOSE 4200

CMD ["npm", "start", "--", "--host", "0.0.0.0"]
