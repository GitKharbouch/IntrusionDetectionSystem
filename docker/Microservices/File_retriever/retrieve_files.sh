# Source and destination directories
source_directory="/app/data/raw_captures"
destination_directory="/app/data/ready_to_process"

# Ensuregit the destination directory exists
mkdir -p "$destination_directory"

# Move all files from the source to the destination
mv "$source_directory"/* "$destination_directory"

# Print a message indicating the operation is complete
echo "Files moved from $source_directory to $destination_directory"
