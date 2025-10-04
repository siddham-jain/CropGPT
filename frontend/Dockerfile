# Frontend Dockerfile
# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build arguments
ARG REACT_APP_BACKEND_URL=http://localhost:8000
ARG REACT_APP_VERSION=1.0.0
ARG REACT_APP_ENVIRONMENT=production

# Set environment variables
ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL
ENV REACT_APP_VERSION=$REACT_APP_VERSION
ENV REACT_APP_ENVIRONMENT=$REACT_APP_ENVIRONMENT

# Build the application
RUN npm run build

# Production stage
FROM nginx:1.25-alpine

# Copy built application
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]