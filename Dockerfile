#FROM continuumio/miniconda3
#RUN conda create -n env python
#RUN echo "source activate env" > ~/.bashrc
#ENV PATH /opt/conda/envs/env/bin:$PATH

FROM python:3.8-slim-buster

WORKDIR /app


RUN apt-get update
RUN apt-get install -y build-essential

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host", "0.0.0.0"]


#steps to run program 
# set cd to python-docker3 directory
#docker-compose -f docker-compose.dev.yml up --build

#to check connection
#curl --request GET --url http://localhost:5000/


#to train:
#curl http://localhost:5000/train


#to get recommendations for a given user:
#curl -d '{"user_id_hash":"b9cbac77a336d62efd54404d2bccaecd"}' -H "Content-Type:application/json" -X POST http://localhost:5000/reco

#output looks like...
#[{"score": [0.7715631723403931, 0.7685680389404297, 0.5186975002288818, 0.0657505989074707, -0.39661741256713867, -0.5397502779960632, -0.6023848056793213, -0.6680276393890381, -0.698615550994873, -0.7386236190795898], "catalog_item_name": ["0a992174178e8303dcfffadef857c776", "0a992174178e8303dcfffadef857c776", "0a992174178e8303dcfffadef857c776", "0a992174178e8303dcfffadef857c776", "0a992174178e8303dcfffadef857c776", "0a992174178e8303dcfffadef857c776", "0a992174178e8303dcfffadef857c776", "0a992174178e8303dcfffadef857c776", "0a992174178e8303dcfffadef857c776", "0a992174178e8303dcfffadef857c776"], "catalog_item_id": ["Bud Light Seltzer Ugly Sweater", "Black Hog Pumpkin Spice Latte Coffee Milk Stout", "Night Shift Phone Home Porter", "Harpoon Black Is Beautiful", "Hennessy Black Cognac Gift Set", "Night Shift Jubilee IPA", "Exhibit 'A' Brewing Company Just A Kitten NEIPA", "Chubini Rkatsiteli Chinuri Orange Wine", "Decoy Limited Napa Valley Cabernet Sauvignon", "Burlington Intangible Tides NEIPA"], "brand_name": [120972, 120108, 117132, 121539, 126130, 113409, 127432, 118995, 115255, 126391]}]