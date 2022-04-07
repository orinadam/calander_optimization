FROM node:17

WORKDIR /app
RUN git clone https://github.com/yalikadman1/calander_optimization.git
WORKDIR /calander_optimization
COPY package*.json ./


RUN npm install

ENV PORT=3000
EXPOSE 3000

CMD ["npm start"]
