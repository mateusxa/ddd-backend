FROM python:3.10

ENV EMAIL_PASSWORD='ksok qfmc xnlp rrhu'
ENV PASSWORD_JWT_SECRET=d00cc638-6e1f-4c1a-b5a9-ae03bd4a525b
ENV ADMIN_JWT_SECRET=e01d3db1-2018-4061-bcdb-a0754fed35d3
ENV CUSTOMER_JWT_SECRET=30622da0-994c-4637-bbe5-f84a9d4f9b87
ENV INVITE_JWT_SECRET=ecd0ee96-3cd5-4c09-96e6-b4815ebbb4e1
ENV DOMAIN=localhost:5000
ENV EMAIL_USER=mateu.xa@gmail.com
ENV TARGET_EMAIL=mateus_xa@hotmail.com

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["waitress-serve", "--port=5000", "app:app"]
