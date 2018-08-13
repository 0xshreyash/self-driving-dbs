import subprocess

def main():
    with open('queries.sql', 'w') as f:
        for i in range(1,11):
            result = subprocess.run(['./qgen', '-r', str(i)], stdout=subprocess.PIPE)
            f.write(result.stdout.decode('utf-8'))

if _name_ == '_main_':
    main()
