# All the imports
import numpy as np
import pandas as pd
from scapy.all import *
from config import *
import json

def extract_features(packets, config, features_dict):
    # Initialize a dictionary to store lists for each variable
    variable_lists = {key: [] for key in config["variables"]}

    # Extract features from each packet
    for packet in packets:
        if IP in packet:
            variable_lists["src_ip"].append(packet[IP].src if IP in packet else 'NA')
            variable_lists["src_port"].append(packet[TCP].sport if TCP in packet else 'NA')
            variable_lists["dst_ip"].append(packet[IP].dst if IP in packet else 'NA')
            variable_lists["dst_port"].append(packet[TCP].dport if TCP in packet else 'NA')
            variable_lists["protocol_type"].append(packet[IP].proto if IP in packet else -1)
            variable_lists["service"].append(packet[TCP].dport if TCP in packet else packet[UDP].dport if UDP in packet else None)
            variable_lists["flag"].append(packet.sprintf("%TCP.flags%") if TCP in packet else 'NA')

            if TCP in packet:
                variable_lists["durations"].append(packet.time - packets[0].time)
                variable_lists["src_bytes"].append(len(packet[TCP].payload))
                variable_lists["dst_bytes"].append(len(packet[IP].payload) - len(packet[TCP].payload))
            elif  UDP in packet:
                variable_lists["durations"].append(packet.time - packets[0].time)
                variable_lists["src_bytes"].append(len(packet[UDP].payload))
                variable_lists["dst_bytes"].append(len(packet[IP].payload) - len(packet[UDP].payload))
            elif ICMP in packet:
                variable_lists["durations"].append(packet.time - packets[0].time)
                icmp_type = packet[ICMP].type
                icmp_code = packet[ICMP].code
                variable_lists["src_bytes"].append(f'Type: {icmp_type}, Code: {icmp_code}')
                variable_lists["dst_bytes"].append('NA')
            else:
                variable_lists["durations"].append('NA')
                variable_lists["src_bytes"].append('NA')
                variable_lists["dst_bytes"].append('NA')

            for key, condition in features_dict.items():
                variable_lists[key].append(evaluate_condition(packet, condition))

    # Check if all lists have the same length
    lengths = set(len(lst) for lst in variable_lists.values())
    if len(lengths) != 1:
        raise ValueError("All arrays must be of the same length")

    df = pd.DataFrame(variable_lists)
    return df

def mapping(df, all_dst_ports, service_mappings,proto_mapping,flag_mapping):
    mapped_services = [service_mappings.get(port, 'other') for port in all_dst_ports]
    service_mappings.update(dict(zip(all_dst_ports, mapped_services)))
    df['service'] = df['service'].map(service_mappings)
    df['protocol_type'] = df['protocol_type'].map(proto_mapping)
    df['flag'] = df['flag'].map(flag_mapping)
    return df

def preprocess_packets(packets, config,features_dict,all_dst_ports,service_mappings,proto_mapping,flag_mapping):
    df = extract_features(packets, config,features_dict)
    df2 = df.copy()
    df2 = df2.drop(['src_ip', 'dst_ip', 'src_port', 'dst_port'], axis=1)
    df2 = mapping(df2,all_dst_ports,service_mappings,proto_mapping,flag_mapping)
    df2 = df2.replace('NA', np.nan)
    df2 = df2.replace('', np.nan)
    df2 = df2.dropna()

    return df2


def evaluate_condition(packet, condition):
    try:
        return eval(condition)
    except:
        return 'NA'

def main():
    # Load configuration from JSON
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        features_dict = config["features"]
        all_dst_ports = config["dst"]["ports"]
        service_mappings = config.get("service_mapping", {})
        service_mappings = {int(key): value for key, value in service_mappings.items()}
        proto_mapping = config.get("protocol_type_mapping", {})
        proto_mapping = {int(key): value for key, value in proto_mapping.items()}
        flag_mapping = config.get("flag_mapping", {})

    # All the data and variables
    packets = rdpcap('traffic-capture-filtered.pcap')
    
    # Preprocess packets
    df = extract_features(packets, config,features_dict)
    df2 = preprocess_packets(packets, config,features_dict,all_dst_ports,service_mappings,proto_mapping,flag_mapping)
    # Save the dataframe to a csv file
    df.to_csv('info_data.csv', index=False)
    df2.to_csv('preprocessed_data.csv', index=False)




if __name__ == "__main__":
    main()