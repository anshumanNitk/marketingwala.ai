# MarketingWala

MarketingWala is a platform that automates the creation and execution of AI-powered marketing campaigns. It streamlines social media post generation with AI-generated images and captions, along with scheduling tools. Additionally, it manages push notifications by generating, scheduling, and executing them seamlessly via Firebase Cloud Messaging, making marketing efforts more efficient and impactful.

:star: Star us on GitHub — it motivates us a lot!

## 🚀 Features  
1. **AI Image and Caption Generation with Scheduling**  
   - Generate social media posts based on product or company information.
   - Provide optional reference images to guide the AI generation process.
   - Review multiple post suggestions and publish directly to social platforms via our app.

2. **Push Notification Generation and Execution**  
   - Create push notifications with AI-generated content.  
   - Schedule and trigger notifications automatically via Firebase Cloud Messaging (FCM).

---

## 🛠️ Tech Stack  
- **Frontend:** React  
- **Backend:** Django  
- **Database:** PostgreSQL  
- **AI Integration:** OpenAI DALL·E 3  
- **API & Hosting:** Cloudflare (@cf/meta/llama-3-8b-instruct)  
- **Orchestration:** Conductor  
- **Notifications:** Firebase Cloud Messaging  
- **Deployment:** AWS S3, GoDaddy for DNS

---

## ⚙️ How It Works  
### Architecture  
- **RESTful API Hosting:** Some APIs are deployed on Cloudflare for enhanced scalability.  
- **Conductor Workflow:**  
  - Manages OAuth 2.0 token renewal and interactions with Firebase Cloud Messaging.  
  - Handles complex workflows like regenerating expired tokens and scheduling notifications.

**Key Workflows:**  
- **Renew OAuth 2.0 Token:**  
  - If tokens are valid: [Check token status](https://play.orkes.io/execution/042992d2-8e9f-11ef-85a8-ba73d777fd9d)  
  - If expired: [Renew tokens](https://play.orkes.io/execution/3d67949b-8e9b-11ef-b6be-323517a1f1a2)  
- **Send Push Notifications:**  
  - Collect mobile users' access tokens via a `GET` request.  
  - Validate or renew tokens if expired.  
  - Send notifications through a `POST` request to Firebase's HTTP v1 API.

---

## 🎉 Try It Out  
Stay tuned for a live demo and deployment details!
