"""Quick script to run the alert generator"""
from batch_alert_generator import AIAlertGenerator

if __name__ == "__main__":
    generator = AIAlertGenerator(use_openai=False)
    generator.generate_alerts()
