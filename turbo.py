import functions
import requests
import os
import json
import urllib.request
import urllib.parse
import os
import time
import threading

claim_queue = []
claiming = []
claimed = []
failed_claim = []
ready = []
claim_accounts = []


def load_claim_account(account, proxy):
    with open(account, 'r') as f:
        for line in f:
            csrf = functions.find_between(line, "csrftoken=", " for")
            mid = functions.find_between(line, "mid=", " for")
            ds_user_id = functions.find_between(line, "ds_user_id=", " for")
            sessionid = functions.find_between(line, "sessionid=", " for")

    cookie = "csrftoken=" + csrf + ";mid=" + mid + \
        ";ds_user_id=" + ds_user_id + ";sessionid=" + sessionid

    getheaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cookie": "" + cookie + ""
    }
    postheaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Accept-Language": "en-US,en;q=0.5",
        "X-CSRFToken": "" + csrf + "",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.instagram.com",
        "Alt-Used": "www.instagram.com",
        "Connection": "keep-alive",
        "Referer": "https://www.instagram.com/accounts/edit/",
        "Cookie": "" + cookie + "",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
    }
    if proxy == "true":
        _user_ = 'spwblik9ka'
        _pass_ = '9Hub2Pbx69gXhkelhF'
        proxy = f"https://{_user_}:{_pass_}@gate.smartproxy.com:10000"
    else:
        proxy = {"http": ""}

    while True:
        try:
            grab = requests.get("https://www.instagram.com/accounts/edit/",
                                headers=getheaders, timeout=10)
            if not grab.text:
                pass
            else:
                break
        except requests.ConnectionError:
            print("[>] Connection timed out. Proxy is probably bad.")
            return

    first_response = grab.text

    biography = functions.find_between(
        str(first_response), '{"biography":"', '",')
    firstname = functions.find_between(
        str(first_response), '"first_name":"', '",')
    email = functions.find_between(str(first_response), '"email":"', '",')
    # email = "Jeff.mariafyz791@rambler.ru"
    phone = functions.find_between(
        str(first_response), '"phone_number":"', '",')
    firstname = functions.unescape(firstname)
    biography = functions.unescape(biography)
    firstname = ""
    biography = ""

    if not email:
        print(functions.CRED +
              "[!] Something went wrong while loading claim account, make sure the account is still valid: " + account)
        return
    else:
        print(functions.CGREEN + "[>] Loaded Claim Account: " + account)
        ready.append("true")
        claim_accounts.append(account)

    while True:
        if not claim_queue:
            time.sleep(2)
        else:
            claim_username = claim_queue[0]
            claiming.append(claim_username)
            print(functions.YELLOW +
                  "[>] Attempting to claim: " + claim_username)
            data1 = 'first_name=' + firstname + '&email=' + urllib.parse.quote(email) + '&username=' + claim_username + '&phone_number=' + urllib.parse.quote(
                phone) + '&biography=' + urllib.parse.quote(biography) + '&external_url=&chaining_enabled=on'
            attempts = 0
            while True:

                if attempts >= 5:
                    print(functions.CRED + "[>] We attempted to claim " +
                          claim_username + " but failed 5 times. Stopping.")
                    failed_claim.append(claim_username)
                    return
                else:
                    pass

                try:
                    send = requests.post("https://www.instagram.com/accounts/edit/",
                                         data=data1, timeout=10, headers=postheaders, proxies={
                                             'http': proxy,
                                             'https': proxy
                                         })
                except requests.ConnectionError:
                    print("[>] Connection timed out. Proxy is probably bad.")
                    return

                try:
                    if not send.text:
                        print(
                            functions.CRED + "[>] Something went wrong getting data from Instagram, retrying")
                    else:
                        pass
                except:
                    pass

                try:
                    if "Something is wrong." in send.text:
                        print(
                            functions.CRED + "[>] Instagram said something was wrong and to try again.")
                        time.sleep(60)
                        attempts += 1
                except:
                    pass

                try:
                    data = json.loads(send.text)
                    if data['status'] == "ok":
                        print(functions.CGREEN + "[>] Successfully claimed username: " +
                              claim_username + " on account: " + account)
                        claimed.append(claim_queue[0])
                        functions.logtofile(
                            "success_turbo_" + claim_username + ".txt", account + " > " + claim_username)
                        claim_queue.remove(claim_username)
                        claiming.remove(claim_username)
                        claim_accounts.remove(account)
                        functions.discordwebbook(
                            "Turbo", account, claim_username)
                        return
                    else:
                        if data['message']['errors'][0] == "This username isn't available. Please try another.":
                            print(functions.CRED +
                                  "[>] %s is not available." % (claim_username))
                            attempts += 1
                        else:
                            if data['status'] == "fail":
                                print(functions.CRED +
                                      "[>] Instagram returned fail.")
                                attempts += 1
                            else:
                                if data['message'] == "Please wait a few minutes before you try again.":
                                    print(functions.CRED + "[>] Rate limited.")
                                    attempts += 1
                                    time.sleep(30)
                                else:
                                    if data['message'] == "feedback_required" or data['feedback_title'] == "Try Again Later":
                                        print(functions.CRED +
                                              "[>] Rate limited #2.")
                                        attempts += 1
                                        time.sleep(30)
                                    else:
                                        if data['message'] == "checkpoint_required":
                                            print(
                                                functions.CRED + "[>] Rate limited #3. (Account might be locked)")
                                            attempts += 1
                                            time.sleep(30)
                except:
                    print(functions.CRED +
                          "[>] Unknown response from Instagram.")


def check_accounts(account, delay, timeout, proxy):
    while True:
        if not ready:
            pass
        else:
            with open(account, 'r') as f:
                for line in f:
                    csrf = functions.find_between(line, "csrftoken=", " for")
                    mid = functions.find_between(line, "mid=", " for")
                    ds_user_id = functions.find_between(
                        line, "ds_user_id=", " for")
                    sessionid = functions.find_between(
                        line, "sessionid=", " for")

            cookie = "csrftoken=" + csrf + ";mid=" + mid + \
                ";ds_user_id=" + ds_user_id + ";sessionid=" + sessionid
            getheaders = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cookie": "" + cookie + ""
            }

            if proxy == "true":
                _user_ = 'spwblik9ka'
                _pass_ = '9Hub2Pbx69gXhkelhF'
                proxy = f"https://{_user_}:{_pass_}@gate.smartproxy.com:10000"
            else:
                proxy = {"http": ""}

            failed = 0
            while True:
                try:
                    if failed >= 50:
                        print(
                            "[>] Closed a thread because we had 50 failed attempts.")
                        return
                except:
                    pass

                with open('files/turbo_usernames.txt', 'r') as accountfile:
                    for username in accountfile:
                        username = username.strip()
                        username = username.replace("\n", "")

                        if username in failed_claim:
                            print(
                                functions.YELLOW + "[>] Skipping %s due to failing earlier or already claimed." % (username))
                        else:
                            pass

                        if not claim_accounts:
                            print(
                                functions.CRED + "[>] You do not have enough claim accounts, please refill folder.")
                            exit()
                        else:
                            pass

                        if username in claim_queue:
                            print(
                                functions.YELLOW + "[>] %s is already in claim queue." % (username))
                        else:
                            try:
                                url = "https://www.instagram.com/" + username + "/"
                                while True:
                                    try:
                                        grab = requests.get(
                                            url, headers=getheaders, timeout=timeout, proxies={
                                                'http': proxy,
                                                'https': proxy
                                            })
                                        if not grab.text:
                                            pass
                                        else:
                                            break
                                    except requests.ConnectionError:
                                        print(
                                            "[>] Connection timed out. Proxy is probably bad.")

                                first_response2 = grab.content
                                check_title = functions.find_between(
                                    str(first_response2), str("<title>"), str("</title>"))
                                check_name = functions.find_between(
                                    str(first_response2), str("\"alternateName\":\""), str("\""))

                                if check_name == "@" + username:
                                    print(
                                        functions.YELLOW+"[>] %s is not available. #1" % (username))
                                else:
                                    if "Posts - See Instagram photos and videos from" in str(first_response2):
                                        print(
                                            functions.YELLOW+"[>] " + username + " is not available. #2")
                                    else:
                                        if "See Instagram photos and videos from " in str(first_response2):
                                            print(
                                                functions.YELLOW+"[>] " + username + " is not available. #3")
                                        else:
                                            if "Create an account or log in to Instagram " in str(first_response2):
                                                print(
                                                    functions.CRED + "[>] Login is bad, get a new one. Most likely locked. #2")
                                                failed += 1
                                                break
                                            else:
                                                if check_title == '\\nInstagram\\n':
                                                    if username in claim_queue:
                                                        print(
                                                            functions.YELLOW + "[>] %s is already in claim queue." % (username))
                                                    else:
                                                        print(
                                                            functions.GREEN+"[>] %s is available, claiming." % (username))
                                                        claim_queue.append(
                                                            username)
                                                else:
                                                    if check_title == '\\nLogin \\xe2\\x80\\xa2 Instagram\\n':
                                                        print(
                                                            functions.CRED+"[>] Login is bad, get a new one. Most likely locked. #3")
                                                        failed += 1
                                                        break
                            except requests.exceptions.Timeout:
                                print(functions.CRED +
                                      "[>] Request timed out.")

                            time.sleep(delay)


def run():
    delay = 3
    timeout = 5

    proxies = "true"

    for filename in os.listdir("turbo_claim"):
        f = os.path.join("turbo_claim", filename)
        if os.path.isfile(f):
            print("[>] Loaded claim account: %s" % (f))
            th = threading.Thread(target=load_claim_account, args=(f, proxies))
            th.start()

    for filename in os.listdir("turbo_check"):
        f = os.path.join("turbo_check", filename)
        if os.path.isfile(f):
            print("[>] Loaded check account: %s" % (f))
            th = threading.Thread(target=check_accounts, args=(
                f, int(delay), int(timeout), proxies))
            th.start()


def turbo():
    # print(functions.CRED + "\n[!] Important Information:")
    # print(functions.YELLOW +
    #       "[>] Place accounts you wish to check usernames from /accounts/ folder into /turbo_check/ folder")
    # print(functions.YELLOW +
    #       "[>] Place accounts you wish to claim usernames from /accounts/ folder into /turbo_claim/ folder.")
    # print(functions.YELLOW +
    #       "[>] Place list of usernames you wish to turbo in /files/turbo_usernames.txt")

    while True:
        files = functions.get_files("turbo_check")
        files2 = functions.get_files("turbo_claim")

        for filename in os.listdir("turbo_claim"):
            f = os.path.join("turbo_claim", filename)
            if os.path.isfile(f):
                with open(f, 'r') as r:
                    for line in r:
                        csrf = functions.find_between(
                            line, "csrftoken=", " for")
                        mid = functions.find_between(line, "mid=", " for")
                        ds_user_id = functions.find_between(
                            line, "ds_user_id=", " for")
                        sessionid = functions.find_between(
                            line, "sessionid=", " for")

        cookie = "csrftoken=" + csrf + ";mid=" + mid + \
            ";ds_user_id=" + ds_user_id + ";sessionid=" + sessionid
        _user_ = 'spwblik9ka'
        _pass_ = '9Hub2Pbx69gXhkelhF'
        proxy = f"https://{_user_}:{_pass_}@gate.smartproxy.com:10000"

        if len(files) <= 0 or len(files2) <= 0:
            print("[!] We could not locate any files in the folder! Make sure the accounts are in the right folder before continuing.")
        else:
            # run()

            turbo_usernames = []
            available_usernames = []

            with open('files/turbo_usernames.txt', 'r') as file:
                for line in file:
                    turbo_usernames.append(line.strip())

            url = f"https://i.instagram.com/api/v1/users/{ds_user_id}/info"
            user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)"

            info = requests.get(url, headers={
                'User-Agent': user_agent
            })

            print(info)

            if not info.text:
                print(
                    functions.CRED + "[>] Something went wrong getting data from Instagram, retrying")

            else:
                pass

            break
