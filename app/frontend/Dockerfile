FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install \
    && adduser -D appuser \
    && chown -R appuser /app

EXPOSE 3000

USER appuser

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
