import socket

def check_redshift_connectivity(host, port):
    try:
        # Create a new socket using the default socket.AF_INET and socket.SOCK_STREAM
        with socket.create_connection((host, port), timeout=10) as sock:
            print(f"Successfully connected to {host} on port {port}")
    except socket.timeout:
        print(f"Connection timed out when attempting to connect to {host} on port {port}")
    except socket.gaierror as e:
        print(f"Address-related error connecting to server: {e}")
    except socket.error as e:
        print(f"Connection error: {e}")

# Hostname and port for the Redshift cluster
host = 'orchestra-cluster-1.ciufpqn7frw8.eu-west-2.redshift.amazonaws.com'
port = 5439  # Default Redshift port

# Run the connectivity check function
check_redshift_connectivity(host, port)
