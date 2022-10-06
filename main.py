from bot import executor, dp

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    # придумать че делать
    # dp.storage.close()
    # dp.storage.wait_closed()
