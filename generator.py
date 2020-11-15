import os

on = True
while on:
    print("[=====================[ GEORGESSL ]=====================]")
    print("[ What would you like to do today?                      ]")
    print("[ 1. Issue a new ROOT CA certificate                    ]")
    print("[ 2. Issue a new intermediate certificate using a CA    ]")
    print("[ 3. Create a cert signed by a root or intermediate CA  ]")
    print("[=======================================================]")
    choice = int(input("[Home]: Please enter an option > "))
    if choice == 1:
        while True:
            ca_name = input("[ROOT CA]: Enter a name for the ROOT CA > ")
            if os.path.isdir(f'./root/{ca_name}'):
                print("Name is taken, try again.")
                break
            else:
                ca_pass = input("[ROOT CA]: Enter a passphrase for this CA > ")
                os.system(f'cd root && mkdir {ca_name} && cd ..')
                stdout = open(f"./root/{ca_name}/passphrase", 'w')
                stdout.write(ca_pass)
                stdout.close()
                os.system(f'openssl genrsa -aes256 -out ./root/{ca_name}/ca.key -passout pass:{ca_pass} 8192')
                print("[ROOT CA]: Finished generating CA key, creating certificate...")
                ca_period = input("[ROOT CA]: Enter the validity period of the certificate in days > ")
                os.system(f'openssl req -sha256 -new -x509 -days {ca_period} -key ./root/{ca_name}/ca.key -out ./root/{ca_name}/ca.crt -passin pass:{ca_pass}')
                os.system(f'cd root && cd {ca_name} && echo 1000 > certserial && echo 1000 > crlnumber && touch certindex && cd ../../')
                fin = open("./templates/ca.conf", "rt")
                fout = open(f"./root/{ca_name}/ca.conf", "wt")
                for line in fin:
                    fout.write(line.replace('%PATH%', f'./root/{ca_name}/'))
                fin.close()
                fout.close()
                break
    elif choice == 2:
        while True:
            inter_name = input("[INTERMEDIATE CA]: Enter a name for the intermediate CA > ")
            if os.path.isdir(f'./intermediate/{inter_name}'):
                print("Name is taken, try again.")
                break
            else:
                os.system(f'cd intermediate && mkdir {inter_name} && cd ..')
                os.system(f'openssl genrsa -out ./intermediate/{inter_name}/intermediate.key 4096')
                os.system(f'openssl req -sha256 -new -key ./intermediate/{inter_name}/intermediate.key -out ./intermediate/{inter_name}/intermediate.csr')
                ca_name = input("[INTERMEDIATE CA]: Enter the name of the root CA to use to sign this certificate > ")
                ca_pass_file = open(f'./root/{ca_name}/passphrase')
                ca_pass = ca_pass_file.readline(0)
                ca_pass_file.close()
                os.system(f'openssl ca -batch -config ./root/{ca_name}/ca.conf -notext -in ./intermediate/{inter_name}/intermediate.csr -out ./intermediate/{inter_name}/intermediate.crt -passin pass:{ca_pass}')
                break
    elif choice == 3:
        while True:
            signed_name = input("[SIGNED]: Enter a name for the signed certificate > ")
            if os.path.isdir(f'./signed/{signed_name}'):
                print("Name is taken, try again.")
                break
            else:
                signed_type = ''
                signed_type_h = ''
                signed_choice = input("[SIGNED]: Is this certificate going to be signed by a ROOT CA or Intermediate CA (r/I) > ")
                if signed_choice.lower() == "r":
                    signed_type = 'root'
                    signed_type_h = 'the ROOT CA'
                else:
                    signed_type = 'intermediate'
                    signed_type_h = 'the intermediate CA'
                signed_ca = input(f"[SIGNED]: Enter name of {signed_type_h} to sign this certificate > ")
                os.system(f'cd signed && mkdir {signed_name} && cd ..')
                os.system(f'openssl genrsa -out ./signed/{signed_name}/cert.key 2048')
                os.system(f'openssl req -new -key ./signed/{signed_name}/cert.key -out ./signed/{signed_name}/cert.csr')
                os.system(f'cp ./templates/extfile.ext ./signed/{signed_name}/cert.ext')
                signed_alt_names = int(input("[SIGNED]: Enter amount of alternative DNS names > "))
                extfile = open(f'./signed/{signed_name}/cert.ext', 'a+')
                for i in range(signed_alt_names):
                    alt_name = input(f'[SIGNED]: Enter alt name {i+1} > ')
                    extfile.write(f"\nDNS.{i+1} = {alt_name}")
                extfile.close()
                signed_days = int(input("[SIGNED]: Enter certificate validity period in days > "))
                os.system(f'openssl x509 -req -in ./signed/{signed_name}/cert.csr -CA ./{signed_type}/{signed_ca}/{signed_type}.crt -CAkey ./{signed_type}/{signed_ca}/{signed_type}.key -CAcreateserial -out ./signed/{signed_name}/cert.crt -days {signed_days} -sha256 -extfile ./signed/{signed_name}/cert.ext')
                break

