import tensorflow as tf
from tensorflow.python.keras import estimator as kes
from tensorflow.python.keras.applications.vgg16 import VGG16
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers import Dropout, Flatten, Dense
from train_model.input_fn import make_input_fn


def create_estimator(params):
    # Import VGG16 model for transfer learning
    base_model = VGG16(weights='imagenet')
    base_model.summary()

    x = base_model.get_layer('fc2').output

    x = Dropout(params['dropout rate'])(x)

    predictions = Dense(params['num classes'], activation="sigmoid", name="sm_out")(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    for layer in model.layers:
        layer.trainable = False

    for layer in model.layers[0: 23]:
        layer.trainable = True

    model.summary()

    model.compile(
        loss="binary_crossentropy",
        optimizer=tf.train.AdamOptimizer(params['learning rate'],
                                         beta1=0.9,
                                         beta2=0.999),
        metrics=["categorical_accuracy"]
    )

    if params['isRunOnCloud']:

        run_config = tf.estimator.RunConfig(
            model_dir=params['output path']
        )
    else:

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.gpu_options.per_process_gpu_memory_fraction = 0.95
        # session_config = tf.contrib.learn.RunConfig(session_config=config)

        run_config = tf.estimator.RunConfig(
            session_config=config,
            model_dir=params['output path']
        )

    # Convert to Estimator (https://cloud.google.com/blog/products/gcp/new-in-tensorflow-14-converting-a-keras-model-to-a-tensorflow-estimator)
    estimator_model = kes.model_to_estimator(
        keras_model=model,
        config=run_config
    )

    return estimator_model


def go_train(params):
    # Create the estimator
    Est = create_estimator(params)

    # Set up Estimator train and evaluation specifications
    train_spec = tf.estimator.TrainSpec(
        input_fn=make_input_fn(params['train csv'], tf.estimator.ModeKeys.TRAIN, params, augment=True),
        max_steps=params['train steps']
    )
    eval_spec = tf.estimator.EvalSpec(
        input_fn=make_input_fn(params['eval csv'], tf.estimator.ModeKeys.EVAL, params, augment=True),
        steps=params['eval steps'],  # Evaluates on "eval steps" batches
        throttle_secs=params['eval_throttle_secs']
    )

    # Set logging level
    tf.logging.set_verbosity(tf.logging.DEBUG)

    print("Starting training and evaluation ...")

    # Run training and evaluation
    tf.estimator.train_and_evaluate(Est, train_spec, eval_spec)

    print("Training and evaluation round is done")


def go_predict(params):
    # Create the estimator
    Est = create_estimator(params)

    # Set logging level
    tf.logging.set_verbosity(tf.logging.DEBUG)

    # Run preduiction
    return Est.predict(input_fn=make_input_fn(params['test csv'], tf.estimator.ModeKeys.PREDICT, params, augment=False))
