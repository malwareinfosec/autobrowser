import time
import psutil
import webbrowser
import argparse


def read_urls_from_file(filename):
  """
  Reads a list of URLs from a text file.

  Args:
      filename: The path to the text file containing URLs.

  Returns:
      A list of URLs read from the file.
  """
  urls = []
  try:
    with open(filename, "r") as f:
      for line in f:
        url = line.strip()  # Remove trailing whitespace
        urls.append(url)
  except FileNotFoundError:
    print(f"Error: File not found - {filename}")
  return urls


def open_urls_in_browser(urls, sleep_time, browser_process_name):
  """
  Opens each URL in a new browser instance and terminates the process
  after the specified sleep time.

  Args:
      urls: A list of URLs to open.
      sleep_time: The time (in seconds) to pause between opening URLs 
                   and killing the browser process.
      browser_process_name: The name of the browser's executable file.
  """
  for index, url in enumerate(urls):
    remaining_urls = len(urls) - (index + 1)
    print(f"Opening URL {index+1} of {len(urls)} ({remaining_urls} remaining)")
    webbrowser.open(url)  # Open URL in a new browser instance
    time.sleep(sleep_time)  # Pause for specified time

    # Find browser processes and kill them (requires psutil library)
    for process in psutil.process_iter():
      if process.name() == browser_process_name:
        try:
          process.kill()
          print(f"Browser process {process.pid} terminated.")
        except psutil.NoSuchProcess:
          pass  # Ignore if process is already gone
    time.sleep(1)


def main():
  """
  Defines default filename, sleep time, and browser process name,
  parses arguments, and calls functions to process URLs.
  """
  default_filename = "urls.txt"
  default_sleep_time = 15  # Set a default sleep time (in seconds)
  default_browser_process_name = "chrome.exe"  # Set a default browser process name (optional, modify if needed)

  # Create argument parser
  parser = argparse.ArgumentParser(description="Open URLs in separate browser instances, wait, and kill processes.")
  parser.add_argument("-f", "--filename", type=str, default=default_filename, help=f"Filename containing URLs (defaults to '{default_filename}')")
  parser.add_argument("-t", "--sleep_time", type=float, default=default_sleep_time, help=f"Time (in seconds) to wait between opening URLs (defaults to {default_sleep_time})")
  parser.add_argument("-b", "--browser", type=str, default=default_browser_process_name, help=f"Browser process name (defaults to '{default_browser_process_name}')")

  # Parse arguments
  args = parser.parse_args()

  # Read URLs from the file
  urls = read_urls_from_file(args.filename)
  if urls:
    open_urls_in_browser(urls, args.sleep_time, args.browser)
    print("All URLs opened and browser processes terminated.")
  else:
    print("No URLs found in the file.")


if __name__ == "__main__":
  main()
