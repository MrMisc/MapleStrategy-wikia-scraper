

@client.command()
async def mstrat(ctx, *argslist):
    args = ''
    try:
        userinput = int(argslist[-1])
        for i in argslist[:-2]:
            args += i + "+"
        args+= argslist[-2]
    except:
        userinput = 5
        for i in argslist[:-1]:
            args += i + "+"
        args+= argslist[-1]
    req = Request(f'https://strategywiki.org/w/index.php?search={args.replace(" ","+")}&title=Special%3ASearch&go=Go')
    # print(f'https://strategywiki.org/w/index.php?search={args.replace(" ","+")}&title=Special%3ASearch&go=Go')
    uClient = urlopen(req)
    soup = BeautifulSoup(uClient.read(), 'html5lib')
    # print(soup)
    stringtoprint, links = Titles(soup)
    await ctx.send(f"`` {stringtoprint} ``")
    def check(m):
        return m.content == m.content and m.author == ctx.author
    morecontent = await client.wait_for('message',check = check, timeout = 40.0)
    faggot = 0
    ans = int(morecontent.content)
    eligible = []
    for i in range(len(soup.find_all('a',{ "class", "result-link"}))):
        eligible.append(i)
    if ans in [x for x in range(len(links))]:
        print(links[ans])
        url = "https://strategywiki.org" + links[ans]
        path = 'C:/Users/Irshad/Pictures/Saved Pictures/newpic.png'
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome('D:/chromedriver.exe',options=options)
        driver.get(url)
        height = driver.execute_script("return document.body.scrollHeight")  #some scrolling to lazy load
        driver.set_window_size(1000, height - 100)
        driver.execute_script("window.scrollTo(0, 100)")
        driver.execute_script("window.scrollTo(0, 0)")
        driver.set_window_size(1000, height)
        userinputtry = 0
        while (True):
            if userinputtry<1000:
                try:
                    numberofpicstomake = min(userinput,height//1000)
                    break
                except:
                    userinputtry+=1
            else:
                numberofpicstomake = min(5,height//1000)
                break
        time.sleep(2) # new images need time to load
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment
        tag = 'body'
        loopcount = 0
        while loopcount<1000:
            try:
                if driver.find_element(By.TAG_NAME, tag).screenshot(path): break
            except Exception:
                print("Looping Till Height")
                loopcount+=1
                tag+=' div'
        driver.quit()
        def long_slice(image_path, out_name, outdir, slice_size):
            """slice an image into parts slice_size tall"""
            img = Image.open(image_path)
            width, height = img.size
            upper = 0
            left = 0
            slices = int(math.ceil(height/slice_size))

            count = 1
            listofsplits = []
            for slice in range(slices):
                #if we are at the end, set the lower bound to be the bottom of the image
                if count == slices:
                    lower = height
                else:
                    lower = int(count * slice_size)
                #set the bounding box! The important bit
                bbox = (left, upper, width, lower)
                working_slice = img.crop(bbox)
                upper += slice_size
                #save the slice
                newpath = f"{outdir}"+ "part" + f"{out_name}" + "_" + str(count)+".png"
                working_slice.save(os.path.join(newpath))
                listofsplits.append(newpath)
                count +=1
            return listofsplits

        # await ctx.send(file=discord.File(path))
        guild = ctx.message.guild
        stringthing = f"tea_mstrat_output"
        await guild.categories[3].create_text_channel(stringthing)
        existing_channel = discord.utils.get(ctx.guild.channels, name=stringthing)
        iden = existing_channel.id
        schannel = client.get_channel(iden)
        await schannel.send(ctx.author.mention)
        for newpath in long_slice(path, "2_split", os.getcwd(), height//numberofpicstomake):
            await schannel.send(file=discord.File(newpath))
            os.remove(newpath)
        os.remove(path)
        time.sleep(180)
        await existing_channel.delete()
