#### 6.20 email from jason hong

**privacy proxy:** 拦截手机network traffict, looks for PII Personal Identifiable information

challenge: PrivacyProxy works better the more users are

opportunity: create global mapping of who knows what about us ...

what kinds of personal data of ours is being sent out, to where, how often, how much



**PII Personal Identifiable Information:**可以甄别个人的信息，如地址、生日、电子邮件、性别、名字、电话信息、电话号码、邮编

##### goal for the summer:

```
- Create a test harness that can download and
   install a given app on phones
   1. https://apps.evozi.com/apk-downloader/#discuss an online service named APK Downloader maybe useful

- Improve our monkey, the script runner that randomly
   explores various screens of an app. Ideally, it would
   also store screenshots of when sensitive data is sent
   out, letting us map out the behaviors of a given app too.

- Run the above on a lot of apps to collect lots of data.
   This will let us get (a) names of keys, (b) likely data
   types (e.g. unique ID, location, MAC address, etc),
   (c) domain names and URIs

- If time allows, create some initial interactive visualizations
   and make the results public.
```

#### Some starting points:

[Who Knows What About Me? A Survey of Behind the Scenes Personal Data Sharing to Third Parties by Mobile Apps](https://techscience.org/a/2015103001/)

but it requires human intervention, which makes it more difficult to scale [10, 22, 43, 45, 46, 47]. 

www.andysbuses.com