import asyncio
import hashlib

async def recv(reader):
    result = ""
    done = False
    while not done:
        data = await reader.read(1024)
        for c in data:
            if c == 0x4:
                done = True
                break
            result += chr(c)
    return result

async def invokeCmd(cmd, reader, writer):
    writer.write(('\x02' + cmd + '\n').encode("utf-8"))
    return await recv(reader)

async def tcp_client(address: str, port: int, password: str, *commands):

    try:
        reader, writer = await asyncio.open_connection(address, port)
    except Exception as e:
        print(e)
        raise Exception("Server is not responding or authorization failed")

    welcResponse = ""
    while 1:
        data = await reader.read(1024)
        welcResponse += data.decode()
        eosPos = welcResponse.find('\n\n')
        if eosPos != -1: break;

    # get seed digest
    prefix = '### Digest seed: '
    seedPos = welcResponse.find(prefix)
    seed = ""

    if seedPos != -1:
        seedPos += len(prefix)
        seedPosEnd = welcResponse.find('\n', seedPos)
        seed = welcResponse[seedPos:seedPosEnd].encode("utf-8")

        md5Obj = hashlib.md5()
        md5Obj.update(seed)
        md5Obj.update(password.encode("utf-8"))
        passHash = md5Obj.hexdigest()

        if await invokeCmd('login ' + passHash, reader, writer) != "Authentication successful, rcon ready.\n":
            raise Exception("Server is not responding or authorization failed")

        results = {}
        for command in commands:
            results[command] = await invokeCmd(command, reader, writer)

        writer.close()
        return results
    else:
        print("Response: " + welcResponse)

    writer.close()
    return None