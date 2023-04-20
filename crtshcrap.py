#! /usr/bin/env python3
import aiohttp
import argparse
import asyncio
from aiohttp import ClientResponse, ClientSession
from sys import argv

timeout = aiohttp.ClientTimeout(total=60)

async def request(url: str, session: ClientSession) -> ClientResponse:
    request = await session.get(url=url)
    return request


async def results(url: str) -> str:
    async with ClientSession() as session:
        response = await request(url, session)
        try:
            return await response.json()
        except Exception as e:
            print("Error Accured", e)
            print("I guess we need to wait :'(")
            exit("")

                  
async def parseResults(keyword: str) -> set:
    url = f"https://crt.sh/?q={keyword}&output=json"
    jsonData = await results(url)
    data = set()
    for segment in jsonData:
        if segment:
            if segment["common_name"]:
                  seg = segment["common_name"]
                  if "*." in seg:
                      data.add(seg[2:])
                  else:
                      data.add(seg)
            if segment["name_value"]:
                  pass
                  segs = segment["name_value"].split()
                  for seg in segs:
                    if "*." in seg:
                      data.add(seg[2:])
                    else:
                        data.add(seg)
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="scraper for crtsh //willing to add more webistes to scrap from// ", formatter_class=argparse.RawDescriptionHelpFormatter, epilog="")
    parser.add_argument("-d", "--domain", help="specify domain target")
    parser.add_argument("-f", "--file", help="specify domains file")
    parser.add_argument("-o", "--output", help="specify output file")
    args = parser.parse_args()
    result = set()
    if len(argv) <= 1:
        parser.print_help()

    if args.domain:
        result = asyncio.run(parseResults(args.domain))
        if args.output:
            file = open(args.output, "w")
            for domain in result:
                print(domain)
                file.write(domain+"\n")
            file.close()
        else:
            for domain in result:
                print(domain)
    
    if args.file:
        file = open(args.file, 'r')
        for line in file:
            result = asyncio.run(parseResults(line))
            if args.output:
                out = open(args.output, "a")
                for domain in result:
                    print(domain)
                    out.write(domain+"\n")
                out.close()
            else:
                for domain in result:
                    print(domain)
        file.close()       

            
