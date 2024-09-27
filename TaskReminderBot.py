from telegram.ext import Updater, CommandHandler, JobQueue
import datetime

# Set an alarm command
def set_alarm(update, context):
    try:
        alarm_time = context.args[0]
        alarm_hour, alarm_minute = map(int, alarm_time.split(':'))
        now = datetime.datetime.now()
        alarm = now.replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)

        if alarm < now:
            alarm += datetime.timedelta(days=1)

        context.job_queue.run_once(alarm_notify, (alarm - now).total_seconds(), context=update.message.chat_id)
        update.message.reply_text(f"Alarm set for {alarm_time}")

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set_alarm HH:MM')

# Notify message
def alarm_notify(context):
    job = context.job
    context.bot.send_message(job.context, text="Did you finish all your tasks?")

# Start command
def start(update, context):
    update.message.reply_text("Hi! Set an alarm using /set_alarm HH:MM.")

# Main function
def main():
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("set_alarm", set_alarm, pass_job_queue=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
