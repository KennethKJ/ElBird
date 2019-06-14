gcloud ml-engine local train \
    --module-name=train_model.task \
    --package-path=${PWD}/train_model \
    -- \
    --batch_size=20 \
    --output_dir="gs://elbird-working-dir/Estimator_Output/6/"