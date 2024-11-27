# Gunakan base image Node.js
FROM node:16-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY package*.json ./
RUN npm install

# Copy semua file
COPY . .

# Expose port untuk backend
EXPOSE 8080

# Jalankan aplikasi
CMD ["node", "app.js"]
