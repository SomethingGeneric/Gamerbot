import aiohttp
import asyncio
import random
import string

# Amount of cats to download
cats = int(input("Cat amount: "))
# URL for random cats
url = "https://cataas.com/cat"
# Each task
tasks = []

# Download an image
async def download(session):
    # Send GET request
    async with session.get(url) as request:
        # Generate file name
        name = "".join(random.sample(string.ascii_lowercase + string.digits, 5))
        # Open the file
        with open(f"./images/cat_{name}.png", "wb") as file:
            # Get each chunk & write
            async for chunk in request.content.iter_chunked(1024):
                file.write(chunk)

        print(f"Cat image downloaded: {name}")


# Start the tasks
async def start():
    # Create a reusable session
    async with aiohttp.ClientSession() as session:
        # Create each task
        for _ in range(cats):
            task = asyncio.ensure_future(download(session))
            tasks.append(task)

        # Start each task
        await asyncio.gather(*tasks)


# Start the start
asyncio.get_event_loop().run_until_complete(start())
