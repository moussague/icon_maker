import base64


icon_path = "app_icon.ico"

with open(icon_path, "rb") as icon_file:
    icon_data = icon_file.read()

base64_icon_data = base64.b64encode(icon_data).decode("utf-8")

output_file_path = "icon_data.py"

with open(output_file_path, "w") as output_file:
    output_file.write(f'icon_data = "{base64_icon_data}"')

print(f"Base64-encoded icon data saved to {output_file_path}")
