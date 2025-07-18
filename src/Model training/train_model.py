from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import inspect

def train(train_dataset, val_dataset, test_dataset, MODEL_NAME, num_labels, label2id, id2label, tokeniser):
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels = num_labels,
        id2label = id2label,
        label2id = label2id      
    )

    print("TrainingArguments is being imported from:", inspect.getfile(TrainingArguments))
    
    training_args = TrainingArguments(
        output_dir='./results',              # Where to save the model
        num_train_epochs=5,                  # Train for 3 full passes over the data
        per_device_train_batch_size=16,      # Use batches of 16 for training
        per_device_eval_batch_size=64,       # Use batches of 64 for evaluation
        eval_strategy="epoch",         # Run evaluation at the end of each epoch
        save_strategy="epoch",               # Save a checkpoint at the end of each epoch
        load_best_model_at_end=True,         # Automatically load the best model when training is done
        logging_steps=10,                    # How often to log training loss
    )

    trainer = Trainer(
        model = model,
        args = training_args,
        train_dataset = train_dataset,
        eval_dataset= val_dataset,
        compute_metrics= compute_metrics,
        tokenizer = tokeniser
    )

    print("Starting training...")
    trainer.train()

    print("\nSaving the best model...")
    trainer.save_model() # This saves the best model to ./results

    # Evaluate the final best model on the unseen test set
    print("\nEvaluating on the test set...")
    test_results = trainer.evaluate(test_dataset)

    print("\nTest Set Results:")
    print(test_results)






def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)

    precision,recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="weighted"
    )
    acc = accuracy_score(labels, preds)

    return {
        "Accuracy ": acc,
        "f1 ": f1,
        "Precision ": precision,
        "Recall ": recall
    }