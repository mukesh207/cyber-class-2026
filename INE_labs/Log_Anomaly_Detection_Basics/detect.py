# Set for storing unique attributes to find anomalies
set_methods = set()
set_dates = set()
set_mon = set()
set_year = set()
num_list = []

# Open the log file and read lines
with open("logs.txt", "r") as f:
    file_content = f.readlines()

# Strip newline characters from each line
file_content = [x.strip() for x in file_content]

# Iterate through each log entry
for line_item in file_content:
    # 1. Tokenize HTTP Method and the rest of the URL
    # Example split: ['CONNECT', 'http://example.net/...']
    token_string = line_item.split(' ')
    set_methods.add(token_string[0])

    # 2. Tokenize the URL parameters
    # Example split: ['http://example.net/access_object.php?param1=1350', 'param2=brachy', 'param3=20APR2013']
    params = token_string[1].split('&')

    # --- Param1 Analysis ---
    # Example: p1 = ['...param1', '1350']
    p1 = params[0].split('=')
    # Store the number as an integer for proper sorting later
    num_list.append(int(p1[1]))

    # --- Param2 Analysis ---
    # Example: p2 = ['param2', 'brachy']
    p2 = params[1].split('=')
    
    # Validation: Check if the string contains the required prefix "brac" (case-insensitive)
    if "brac" not in str(p2[1]).lower():
        print("[!] Anomalous entry found in param2: " + str(p2[1]))

    # --- Param3 Analysis ---
    # Example: p3 = ['param3', '20APR2013']
    p3 = params[2].split('=')
    date_str = p3[1]
    
    # Slicing the date string to extract DD, MMM, and YYYY
    set_dates.add(date_str[0:2])
    set_mon.add(date_str[2:5])
    set_year.add(date_str[5:])

# --- Output the sets to identify anomalies manually ---

print("\n--- Result Analysis ---")
print("[*] HTTP Methods observed: " + str(set_methods))
print("[*] Days observed: " + str(set_dates))
print("[*] Months observed: " + str(set_mon))
print("[*] Years observed: " + str(set_year))

# --- Outlier detection for Param1 ---
num_list.sort()
# Uncomment the line below to print the sorted list. 
# Due to the large volume of data, you'll want to look at the very beginning and very end of the list for outliers.
# print("[*] Sorted Param1 values: " + str(num_list))
