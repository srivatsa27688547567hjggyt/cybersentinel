# 🛡️ CyberSentinel - AI Cybersecurity Toolkit

CyberSentinel is a powerful, AI-driven cybersecurity monitoring toolkit that combines real-time log analysis, threat detection, and IP intelligence in one comprehensive solution.

## ✨ Features

- **🧠 AI-Powered Threat Detection**: Utilizes Mixtral-8x7B-Instruct model for intelligent threat analysis and classification
- **📡 Real-Time Log Monitoring**: Live monitoring of system logs with persistent storage
- **🌐 IP Intelligence**: Track and visualize IP locations with detailed geographic information
- **⚠️ Threat Classification**: AI-based classification of potential security threats
- **📊 Interactive Dashboard**: Streamlit-based UI for easy monitoring and analysis

## 🚀 Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔑 API Key Setup

The application uses the Together AI API for threat analysis. You'll need to:

1. Get your API key from [Together AI](https://www.together.ai)
2. Replace the `TOGETHER_API_KEY` in `app.py` with your key

## 💻 Usage

Start the application:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501` with the following features:

### Dashboard
- Overview of system security status
- Real-time monitoring statistics

### Threat Detector
- Input suspicious IPs, file hashes, or threat descriptions
- Get AI-powered analysis and explanations

### Live Monitor
- Real-time system log monitoring
- Persistent log storage for historical analysis

### Threat Classifier
- Paste suspicious logs or behaviors
- Get detailed threat classifications

### IP Tracker
- Track and visualize IP locations
- View historical IP lookup data
- Geographic visualization with interactive maps

## 🔧 Technical Stack

- **Frontend**: Streamlit
- **Database**: SQLite with SQLAlchemy ORM
- **AI Model**: Mixtral-8x7B-Instruct via Together AI
- **Geolocation**: IPInfo.io API
- **Visualization**: Folium for map rendering

## 📝 Dependencies

- streamlit==1.34.0
- scikit-learn==1.4.2
- pandas==2.2.2
- numpy==1.26.4
- transformers==4.40.2
- requests==2.31.0
- python-dotenv==1.0.1
- ipwhois

## 🔒 Security Note

Make sure to:
- Keep your API keys secure
- Monitor log file permissions
- Regularly update dependencies
- Review IP tracking data retention policies

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.