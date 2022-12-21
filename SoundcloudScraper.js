//imports
const puppeteer = require('puppeteer-extra');
const hidden = require('puppeteer-extra-plugin-stealth')
const fs = require('fs');
// require executablePath from puppeteer
const {executablePath} = require('puppeteer')

main()

async function main() {

  // Launch sequence
  puppeteer.use(hidden())
  const browser = await puppeteer.launch({
    args: ['--no-sandbox',],
    headless: false,
    ignoreHTTPSErrors: true,
    executablePath: executablePath(),
  })
  //opening new page
  const page = await browser.newPage()
  await page.setViewport({
    width: 1366,
    height: 768,
    deviceScaleFactor: 1,
  });
  //going to soundcloud likes
  await page.goto('https://soundcloud.com/you/likes', {
    waitUntil: 'networkidle0',
  });

  //login process 
  await page.waitForFunction(() => {
    const username = confirm('Please complete login process (20 seconds)')
    return username
  });
  //allowing user 20 seconds to type user and password
  await page.waitForTimeout(20000)
  //if user is still on login page then user has to restart program
  if (page.url().includes("redirect")) {
    await page.waitForFunction(() => {
      const username = confirm('Login not completed in time Restart program')
      return username
    });
  }
  //refreshes the page
  await page.reload({ waitUntil: ["networkidle0", "domcontentloaded"] });
  //scroll all the way down to get all the liked songs
  for (let i = 0; i < 180000; i++){
    await page.keyboard.down('End')
  }
  await page.waitForTimeout(5000)

  //collecting all the hrefs of each artist from each song
  const hrefs = await page.evaluate(() => Array.from(document.querySelectorAll('.audibleTile__usernameHeading'), element => element.getAttribute('href')));
  //file to import to 
  const fileName = "data.txt"
  //collection of all the data
  let data= "Artist;Followers\n"
  //disallows for the program to timeout
  await page.setDefaultNavigationTimeout(0); 

  //visiting each href and appending to the data
  for (let i = 0; i < hrefs.length; i++) {
    await page.goto('https://soundcloud.com'+hrefs[i],{ 
      waitUntil: ["networkidle0", "domcontentloaded"] 
    
    })
    const element = await page.$('.infoStats__value')
    //getting num of followers
    const value = await page.evaluate(el => el.textContent, element)
    data += hrefs[i].substring(1) + ";" + value +"\n"
  }
  //writing to file
  fs.writeFile(fileName, data, (err) => {
    if (err) throw err;
  })
  //browser.close()
} 
