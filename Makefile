.PHONY: run run-container gcloud-deploy

run:
	@streamlit run main.py --server.port=8080

run-container:
	@docker build . -t app.py
	@docker run -p 8080:8080 app.py

gcloud-deploy:
	@gcloud config set project Veiled-Chess
	@gcloud app deploy app.yaml --stop-previous-version