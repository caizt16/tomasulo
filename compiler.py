def run_code(code):
    code_list = code.strip('\n').split(',')
    if code_list[0] == 'LD':
        return

def main():
    run_code('LD, F1, 0xc')

if __name__ == '__main__':

