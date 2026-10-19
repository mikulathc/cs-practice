import sys
from stats import read_valid, average_by_city, warmest_city

def main():
    raw_lines = sys.stdin.read().splitlines()
    
    # Считаем непустые строки (они могут быть либо хорошими, либо ошибочными)
    non_empty_lines = [line for line in raw_lines if line.strip()]
    total_non_empty = len(non_empty_lines)
    
    valid_records = read_valid(raw_lines)
    count_parsed = len(valid_records)
    
    # Ошибки = все непустые минус те, что успешно распарсились
    count_skipped = total_non_empty - count_parsed
    
    if count_parsed == 0:
        print(0)
        print(count_skipped)
        print(0.0)
        return

    warmest = warmest_city(valid_records)
    avg_temp_map = average_by_city(valid_records)
    result_temp = avg_temp_map[warmest]
    
    print(count_parsed)
    print(count_skipped)
    print(f"{result_temp:.1f}")

if __name__ == "__main__":
    main()


