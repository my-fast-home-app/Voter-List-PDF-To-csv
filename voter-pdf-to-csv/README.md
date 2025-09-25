# PDF to CSV Converter - ভোটার তালিকা

এটি একটি Flask-based web application যা ভোটার তালিকার PDF ফাইলকে CSV ফাইলে রূপান্তর করে।

## স্থানীয়ভাবে চালানোর জন্য

1. রিপোজিটরি ক্লোন করুন:
```bash
git clone <your-repo-url>
cd voter-pdf-to-csv
```

2. ভার্চুয়াল এনভায়রনমেন্ট তৈরি করুন:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. প্রয়োজনীয় প্যাকেজ ইন্সটল করুন:
```bash
cd app
pip install -r requirements.txt
```

4. অ্যাপ্লিকেশন চালু করুন:
```bash
python app.py
```

5. ব্রাউজারে যান: http://localhost:5000

---

## Azure-এ ডেপ্লয় করার জন্য

**Prerequisites:**
- Azure Account
- Azure Container Registry (ACR)
- Azure Web App for Containers

**Steps:**

1. Azure Pipeline কনফিগার করুন:
   - Azure DevOps-এ নতুন প্রোজেক্ট তৈরি করুন
   - এই রিপোজিটরি কানেক্ট করুন
   - Pipeline তৈরি করুন এবং azure-pipelines.yml ফাইল সিলেক্ট করুন
2. Azure Resources তৈরি করুন:
   ```bash
   # Resource Group
   az group create --name myResourceGroup --location eastus
   
   # Container Registry
   az acr create --resource-group myResourceGroup --name myacr --sku Basic
   
   # App Service Plan
   az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux
   
   # Web App
   az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name voter-pdf-converter --deployment-container-image-name myacr.azurecr.io/voter-pdf-to-csv:latest
   ```
3. Environment Variables সেট করুন:
   ```bash
   az webapp config appsettings set --resource-group myResourceGroup --name voter-pdf-converter --settings WEBSITES_PORT=5000
   ```

---

## Features

- PDF ফাইল আপলোড
- ড্র্যাগ এন্ড ড্রপ সাপোর্ট
- রিয়েল-টাইম প্রোগ্রেস ইন্ডিকেটর
- CSV ফাইল ডাউনলোড
- রেস্পন্সিভ ডিজাইন

## Technology Stack

- Backend: Python, Flask, pdfplumber, pandas
- Frontend: HTML5, CSS3, JavaScript, Bootstrap
- Deployment: Docker, Azure Container Registry, Azure Web App
- CI/CD: Azure Pipelines

---

এই সম্পূর্ণ সেটআপটি Azure-এ ডেপ্লয় করার জন্য প্রস্তুত। আপনাকে শুধু Azure subscription এবং Azure DevOps account সেটআপ করতে হবে।
