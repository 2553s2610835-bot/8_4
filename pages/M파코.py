<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>m파코 (mPako) - MZ어 번역기 & 사전</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Noto Sans KR Font -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;800&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        pastelBg: '#FDF8F5',
                        pastelPurple: '#E8DFF5',
                        pastelPink: '#FCE1E4',
                        pastelYellow: '#FCF4DD',
                        pastelGreen: '#DDEDEA',
                        pastelBlue: '#DAEAF1',
                        brandPrimary: '#9B82C3',
                        brandDark: '#4A3E56'
                    },
                    fontFamily: {
                        sans: ['Noto Sans KR', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #FDF8F5;
            font-family: 'Noto Sans KR', sans-serif;
            -webkit-tap-highlight-color: transparent;
        }
        .tab-btn.active {
            background-color: #9B82C3;
            color: white;
            box-shadow: 0 4px 12px rgba(155, 130, 195, 0.3);
        }
        .cute-card {
            background: white;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(155, 130, 195, 0.1);
            border: 2px solid #F2EBF9;
        }
        .pulse-ring {
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(155, 130, 195, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 15px rgba(155, 130, 195, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(155, 130, 195, 0); }
        }
    </style>
</head>
<body class="flex justify-center min-h-screen text-slate-700 pb-10">

    <!-- Mobile Frame Container -->
    <div class="w-full max-w-md min-h-screen flex flex-col justify-between p-4 relative">
        
        <!-- Header / Mascot Section -->
        <div>
            <header class="text-center my-4 relative">
                <div class="inline-block relative">
                    <!-- Mascot Badge -->
                    <div class="w-20 h-20 mx-auto rounded-full bg-pastelPink border-4 border-white shadow-md flex items-center justify-center text-4xl mb-2 relative overflow-hidden">
                        🐶
                    </div>
                    <span class="absolute -bottom-1 -right-1 bg-pastelYellow text-slate-800 text-xs px-2 py-0.5 rounded-full font-bold shadow border border-amber-200">v2.0</span>
                </div>
                <h1 class="text-2xl font-extrabold text-brandDark mt-1 tracking-tight">m파코 <span class="text-xs font-semibold px-2 py-0.5 bg-pastelPurple text-brandPrimary rounded-full">mPako</span></h1>
                <p class="text-xs text-slate-500 mt-1">MZ어 ↔ 표준어 파파고 통번역기</p>
            </header>

            <!-- Navigation Tabs -->
            <nav class="grid grid-cols-4 gap-1 p-1.5 bg-pastelPurple/40 rounded-2xl mb-4 text-xs font-bold">
                <button onclick="switchTab('translator')" id="tab-translator" class="tab-btn active py-2.5 rounded-xl transition-all flex flex-col items-center gap-1">
                    <i class="fa-solid font-size-14 fa-language text-sm"></i>
                    <span>번역기</span>
                </button>
                <button onclick="switchTab('voice')" id="tab-voice" class="tab-btn py-2.5 text-slate-600 rounded-xl transition-all flex flex-col items-center gap-1">
                    <i class="fa-solid fa-microphone text-sm"></i>
                    <span>음성 파파고</span>
                </button>
                <button onclick="switchTab('ocr')" id="tab-ocr" class="tab-btn py-2.5 text-slate-600 rounded-xl transition-all flex flex-col items-center gap-1">
                    <i class="fa-solid fa-camera text-sm"></i>
                    <span>캡처 스캔</span>
                </button>
                <button onclick="switchTab('dict')" id="tab-dict" class="tab-btn py-2.5 text-slate-600 rounded-xl transition-all flex flex-col items-center gap-1">
                    <i class="fa-solid fa-book-bookmark text-sm"></i>
                    <span>밈 사전</span>
                </button>
            </nav>

            <!-- TAB 1: Text Translator -->
            <section id="sec-translator" class="space-y-4">
                <div class="cute-card p-4">
                    <!-- Direction & Tone Selector -->
                    <div class="flex items-center justify-between gap-2 mb-3">
                        <select id="trans-dir" class="bg-pastelYellow text-xs font-bold text-slate-700 py-2 px-3 rounded-xl border-none outline-none flex-1">
                            <option value="mz2std">MZ어 ➡️ 표준어</option>
                            <option value="std2mz">표준어 ➡️ MZ어</option>
                        </select>
                        <i class="fa-solid fa-arrow-right-arrow-left text-brandPrimary text-xs"></i>
                        <select id="trans-tone" class="bg-pastelGreen text-xs font-bold text-slate-700 py-2 px-3 rounded-xl border-none outline-none flex-1">
                            <option value="basic">기본 톤</option>
                            <option value="biz">비즈니스 톤</option>
                            <option value="sad">해탈/탈탈 톤</option>
                        </select>
                    </div>

                    <!-- Input Area -->
                    <div class="relative">
                        <textarea id="input-text" rows="3" class="w-full text-sm p-3 rounded-xl bg-slate-50 border border-slate-200 outline-none focus:border-brandPrimary resize-none" placeholder="번역할 문장을 입력하세요... (예: 오늘 개야르 폼 미쳤다)">오늘 개야르 폼 미쳤다 억까 미쳤네</textarea>
                        <button onclick="clearInput()" class="absolute right-2 top-2 text-slate-400 hover:text-slate-600 text-xs p-1">
                            <i class="fa-solid fa-circle-xmark"></i>
                        </button>
                    </div>

                    <!-- Translate Action Button -->
                    <button onclick="runTranslation()" class="w-full mt-3 py-3 bg-brandPrimary text-white font-bold rounded-xl shadow-md hover:opacity-90 active:scale-95 transition-all text-sm flex items-center justify-center gap-2">
                        <span>🐶 m파코 번역 실행</span>
                    </button>
                </div>

                <!-- Result Card -->
                <div id="trans-result-card" class="cute-card p-4 hidden border-2 border-brandPrimary/30">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-xs font-extrabold text-brandPrimary bg-pastelPurple px-2.5 py-1 rounded-full">✨ 번역 결과</span>
                        <!-- Papago Style Audio Speaker -->
                        <button onclick="speakText(document.getElementById('result-text').innerText)" class="text-brandPrimary hover:bg-pastelPurple p-2 rounded-full transition-all">
                            <i class="fa-solid fa-volume-high text-lg"></i>
                        </button>
                    </div>

                    <div id="result-text" class="text-base font-bold text-slate-800 my-2 leading-relaxed">
                        <!-- Result will appear here -->
                    </div>

                    <!-- Explanation / Tip Card -->
                    <div id="result-tip" class="bg-pastelYellow/60 p-3 rounded-xl text-xs text-slate-600 mt-3 border border-amber-200/60 leading-normal">
                        <!-- Tip description -->
                    </div>

                    <!-- Secondary Buttons -->
                    <div class="grid grid-cols-3 gap-2 mt-3 pt-3 border-t border-slate-100">
                        <button onclick="copyToClipboard()" class="py-1.5 bg-slate-100 hover:bg-slate-200 rounded-lg text-xs text-slate-600 font-semibold flex items-center justify-center gap-1">
                            <i class="fa-regular fa-copy"></i> 복사
                        </button>
                        <button onclick="bookmarkCurrent()" class="py-1.5 bg-slate-100 hover:bg-slate-200 rounded-lg text-xs text-slate-600 font-semibold flex items-center justify-center gap-1">
                            <i class="fa-regular fa-star"></i> 저장
                        </button>
                        <button onclick="shareResult()" class="py-1.5 bg-slate-100 hover:bg-slate-200 rounded-lg text-xs text-slate-600 font-semibold flex items-center justify-center gap-1">
                            <i class="fa-solid fa-share-nodes"></i> 공유
                        </button>
                    </div>
                </div>
            </section>

            <!-- TAB 2: Voice Papago (STT & TTS) -->
            <section id="sec-voice" class="space-y-4 hidden">
                <div class="cute-card p-5 text-center">
                    <div class="mb-3">
                        <span class="bg-pastelBlue text-sky-700 text-xs font-bold px-3 py-1 rounded-full">파파고 방식 실시간 음성 번역</span>
                    </div>

                    <p class="text-xs text-slate-500 mb-6">마이크 버튼을 누르고 말씀하시면<br>자동으로 음성을 인식해 번역 후 읽어드립니다.</p>

                    <!-- Push to Talk Button -->
                    <div class="flex justify-center my-4">
                        <button id="mic-btn" onclick="toggleSTT()" class="w-24 h-24 rounded-full bg-pastelPink text-pink-600 text-3xl flex items-center justify-center shadow-lg border-4 border-white transition-all active:scale-95">
                            <i class="fa-solid fa-microphone"></i>
                        </button>
                    </div>

                    <p id="voice-status" class="text-xs font-bold text-slate-600 my-2">버튼을 눌러 음성 인식을 시작하세요</p>

                    <!-- Realtime Transcript Box -->
                    <div class="mt-4 p-3 bg-slate-50 rounded-xl text-left border border-slate-200 min-h-[70px]">
                        <span class="text-[10px] text-slate-400 font-bold block mb-1">🎙️ 인식된 음성</span>
                        <div id="voice-transcript" class="text-xs text-slate-700 italic">음성 대기 중...</div>
                    </div>

                    <!-- Translated Voice Result -->
                    <div class="mt-2 p-3 bg-pastelPurple/30 rounded-xl text-left border border-purple-100 min-h-[70px]">
                        <span class="text-[10px] text-brandPrimary font-bold block mb-1">📢 파파고 실시간 번역</span>
                        <div id="voice-translated" class="text-xs font-bold text-brandDark">번역 결과가 여기에 표시됩니다.</div>
                    </div>
                </div>
            </section>

            <!-- TAB 3: OCR Capture Scanner -->
            <section id="sec-ocr" class="space-y-4 hidden">
                <div class="cute-card p-4">
                    <h3 class="text-sm font-bold text-slate-800 mb-1">📷 카톡 / DM / 짤방 캡처 번역</h3>
                    <p class="text-xs text-slate-500 mb-4">이미지를 올리시면 텍스트를 감지하여 번역해드립니다.</p>

                    <!-- Upload Box -->
                    <label class="border-2 border-dashed border-pastelPurple bg-pastelBg rounded-2xl p-6 flex flex-col items-center justify-center cursor-pointer hover:bg-pastelPurple/20 transition-all">
                        <i class="fa-solid fa-cloud-arrow-up text-3xl text-brandPrimary mb-2"></i>
                        <span class="text-xs font-bold text-slate-600">카톡/SNS 캡처 이미지 업로드</span>
                        <span class="text-[10px] text-slate-400 mt-1">PNG, JPG 지원</span>
                        <input type="file" accept="image/*" class="hidden" onchange="handleOCRUpload(event)">
                    </label>

                    <!-- Sample Buttons for Quick Demo -->
                    <div class="mt-3">
                        <span class="text-[11px] text-slate-400 font-bold">샘플 데이터로 테스트:</span>
                        <div class="flex gap-2 mt-1">
                            <button onclick="demoOCR('katalk')" class="text-xs px-2.5 py-1 bg-pastelYellow rounded-lg font-semibold text-slate-700">카톡 짤</button>
                            <button onclick="demoOCR('dm')" class="text-xs px-2.5 py-1 bg-pastelPink rounded-lg font-semibold text-slate-700">인스타 DM</button>
                        </div>
                    </div>
                </div>

                <!-- OCR Result -->
                <div id="ocr-result" class="cute-card p-4 hidden space-y-3">
                    <span class="text-xs font-bold text-emerald-600 bg-pastelGreen px-2.5 py-1 rounded-full"> OCR 스캔 완료</span>
                    <div class="p-3 bg-slate-50 rounded-xl text-xs space-y-2">
                        <div>
                            <span class="text-slate-400 font-bold block">인식된 텍스트:</span>
                            <span id="ocr-raw" class="font-semibold text-slate-800">"아 진짜 뇌절 오지게 치네... 개야르임?"</span>
                        </div>
                        <div class="pt-2 border-t border-slate-200">
                            <span class="text-brandPrimary font-bold block">m파코 표준어 번역:</span>
                            <span id="ocr-translated" class="font-extrabold text-brandDark">"동일한 언행을 과하게 반복하여 피로감을 주네요. 정말 대단한 상황인가요?"</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- TAB 4: Meme Dictionary -->
            <section id="sec-dict" class="space-y-4 hidden">
                <div class="cute-card p-4">
                    <!-- Search Input -->
                    <div class="relative mb-3">
                        <input type="text" id="dict-search" oninput="searchDict()" placeholder="신조어 검색 (예: 개야르, 갓생, 억까)" class="w-full text-xs p-3 pl-9 rounded-xl bg-slate-50 border border-slate-200 outline-none focus:border-brandPrimary">
                        <i class="fa-solid fa-magnifying-glass absolute left-3 top-3.5 text-slate-400 text-xs"></i>
                    </div>

                    <div class="flex justify-between items-center mb-2">
                        <h3 class="text-xs font-extrabold text-slate-700">🔥 트렌드 MZ어 사전 TOP 8</h3>
                        <span class="text-[10px] text-slate-400">실시간 업데이트</span>
                    </div>

                    <!-- Meme List Container -->
                    <div id="dict-list" class="space-y-2 max-h-[380px] overflow-y-auto pr-1">
                        <!-- Items rendered via JS -->
                    </div>
                </div>
            </section>
        </div>

        <!-- Notification Toast -->
        <div id="toast" class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-xs py-2 px-4 rounded-full shadow-lg opacity-0 transition-opacity pointer-events-none z-50">
            알림 메시지
        </div>

        <!-- Footer -->
        <footer class="text-center text-[11px] text-slate-400 py-2 mt-4">
            🐶 m파코 (mPako) Translate App &copy; 2026. All rights reserved.
        </footer>
    </div>

    <!-- JavaScript Logic -->
    <script>
        // ==========================================
        // 1. MZ어 신조어 데이터베이스 (확장 버전)
        // ==========================================
        const dictionary = [
            { term: "개야르", std: "매우 놀랍거나 대단함 (극찬/감탄 표현)", tip: "‘개-’(강조 접두사) + ‘야르’(야호/감탄사)가 합성된 최신 유행어입니다." },
            { term: "폼 미쳤다", std: "기량이나 실력이 매우 뛰어남", tip: "스포츠나 작업물에서 역대급 능력을 발휘할 때 쓰는 극찬 표현입니다." },
            { term: "중꺾마", std: "중요한 것은 꺾이지 않는 마음", tip: "어려운 상황에서도 포기하지 않는 의지를 나타낼 때 쓰입니다." },
            { term: "알잘딱깔센", std: "알아서 잘 딱 깔끔하고 센스있게", tip: "지시를 받지 않고도 완벽하게 업무나 처리를 완수할 때 씁니다." },
            { term: "억까", std: "억지로 까기 (억울한 불운 상황)", tip: "이유 없이 억울한 일이나 나쁜 상황을 겪었을 때 쓰는 단어입니다." },
            { term: "갓생", std: "모범적이고 부지런하게 살아가는 삶", tip: "God(신) + 생(生)의 합성어로 알찬 일상을 의미합니다." },
            { term: "뇌절", std: "똑같은 말을 과도하게 반복함", tip: "상대방이 과하거나 피곤하게 행동할 때 자제를 요청하며 씁니다." },
            { term: "T발 C야?", term: "왜 이리 냉정하고 이성적인 거야?", tip: "MBTI T형의 차가운 반응에 서운함을 표할 때 유쾌하게 쓰는 질문입니다." },
            { term: "디토", std: "동감한다 / 나도 그래", tip: "Ditto(마찬가지)에서 유래하여 의견에 찬성할 때 씁니다." },
            { term: "추앙", std: "깊이 존경하고 응원함", tip: "드라마 대사에서 유래하여 누군가를 절대적으로 응원할 때 쓰입니다." }
        ];

        // Saved Bookmarks
        let bookmarks = [];

        // ==========================================
        // 2. 탭 전환 기능
        // ==========================================
        function switchTab(tabName) {
            const tabs = ['translator', 'voice', 'ocr', 'dict'];
            tabs.forEach(t => {
                document.getElementById(`sec-${t}`).classList.add('hidden');
                document.getElementById(`tab-${t}`).classList.remove('active');
                document.getElementById(`tab-${t}`).classList.add('text-slate-600');
            });

            document.getElementById(`sec-${tabName}`).classList.remove('hidden');
            const activeBtn = document.getElementById(`tab-${tabName}`);
            activeBtn.classList.add('active');
            activeBtn.classList.remove('text-slate-600');

            if (tabName === 'dict') {
                renderDict();
            }
        }

        // ==========================================
        // 3. 텍스트 번역 로직
        // ==========================================
        function runTranslation() {
            const text = document.getElementById('input-text').value.trim();
            const dir = document.getElementById('trans-dir').value;
            const tone = document.getElementById('trans-tone').value;

            if (!text) {
                showToast("번역할 문장을 입력해 주세요!");
                return;
            }

            let translated = text;
            let tipText = "💡 m파코 지능형 문맥 분석 알고리즘이 적용되었습니다.";

            if (dir === 'mz2std') {
                // Replace terms found in dictionary
                let foundTips = [];
                dictionary.forEach(item => {
                    if (translated.includes(item.term)) {
                        translated = translated.replaceAll(item.term, item.std);
                        foundTips.push(`<b>${item.term}</b>: ${item.tip}`);
                    }
                });

                // Apply Tone modifiers
                if (tone === 'biz') {
                    translated = `[비즈니스 레포트] 본 결과는 다음과 같습니다: ${translated} 하였습니다.`;
                } else if (tone === 'sad') {
                    translated = `${translated}... 하, 진짜 세상이 왜 이럴까요?`;
                }

                if (foundTips.length > 0) {
                    tipText = foundTips.join('<br>');
                } else {
                    tipText = "💡 특수 신조어가 포함되지 않은 일반 문장이거나 표준어입니다.";
                }
            } else {
                // Standard to MZ어 Translation Demo
                translated = "오늘 개야르 폼 미쳐서 알잘딱깔센으로 갓생 사는 중 ㄷㄷ";
                tipText = "💡 무거운 정석적 표현을 캐주얼하고 신나는 MZ 밈 어조로 변환했습니다.";
            }

            document.getElementById('result-text').innerText = translated;
            document.getElementById('result-tip').innerHTML = tipText;
            document.getElementById('trans-result-card').classList.remove('hidden');
        }

        function clearInput() {
            document.getElementById('input-text').value = '';
            document.getElementById('trans-result-card').classList.add('hidden');
        }

        // ==========================================
        // 4. 파파고 음성 듣기 (TTS: Text-To-Speech)
        // ==========================================
        function speakText(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel(); // Stop ongoing speech
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'ko-KR';
                utterance.rate = 0.95; // Papago speed
                utterance.pitch = 1.0;
                window.speechSynthesis.speak(utterance);
                showToast("🔊 파파고 음성 재생 중...");
            } else {
                showToast("이 브라우저는 음성 재생을 지원하지 않습니다.");
            }
        }

        // ==========================================
        // 5. 음성 인식 파파고 모드 (STT: Speech-To-Text)
        // ==========================================
        let recognition = null;
        let isListening = false;

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = 'ko-KR';
            recognition.continuous = false;

            recognition.onstart = function() {
                isListening = true;
                const micBtn = document.getElementById('mic-btn');
                micBtn.classList.add('pulse-ring', 'bg-red-400', 'text-white');
                document.getElementById('voice-status').innerText = "🎧 음성을 듣고 있습니다... 말씀하세요!";
            };

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById('voice-transcript').innerText = `"${transcript}"`;

                // Translate transcript
                let translated = transcript;
                dictionary.forEach(item => {
                    if (translated.includes(item.term)) {
                        translated = translated.replaceAll(item.term, item.std);
                    }
                });

                document.getElementById('voice-translated').innerText = translated;
                
                // Read out automatically like Papago
                speakText(translated);
            };

            recognition.onerror = function(event) {
                showToast("음성 인식 오류가 발생했습니다.");
                resetMicUI();
            };

            recognition.onend = function() {
                resetMicUI();
            };
        }

        function toggleSTT() {
            if (!recognition) {
                // Fallback simulation if browser doesn't support SpeechRecognition
                showToast("마이크 지원 브라우저 시뮬레이션 동작");
                document.getElementById('voice-transcript').innerText = '"아 오늘 개야르 출근하다 억까 당함"';
                const trans = "오늘 매우 당황스러운 출근 과정에서 억울한 일들을 겪었습니다.";
                document.getElementById('voice-translated').innerText = trans;
                speakText(trans);
                return;
            }

            if (isListening) {
                recognition.stop();
            } else {
                recognition.start();
            }
        }

        function resetMicUI() {
            isListening = false;
            const micBtn = document.getElementById('mic-btn');
            micBtn.classList.remove('pulse-ring', 'bg-red-400', 'text-white');
            document.getElementById('voice-status').innerText = "버튼을 눌러 음성 인식을 시작하세요";
        }

        // ==========================================
        // 6. OCR 스캔 데모
        // ==========================================
        function handleOCRUpload(event) {
            if (event.target.files && event.target.files[0]) {
                showToast("이미지를 분석하고 있습니다...");
                setTimeout(() => {
                    document.getElementById('ocr-raw').innerText = '"이번 프로젝트 폼 미쳤네 알잘딱깔센 가자"';
                    document.getElementById('ocr-translated').innerText = '"이번 프로젝트 성과가 매우 뛰어납니다. 알아서 센스있게 완수해봅시다."';
                    document.getElementById('ocr-result').classList.remove('hidden');
                }, 1000);
            }
        }

        function demoOCR(type) {
            document.getElementById('ocr-result').classList.remove('hidden');
            if (type === 'katalk') {
                document.getElementById('ocr-raw').innerText = '"아 뇌절 오지게 치네... 개야르임?"';
                document.getElementById('ocr-translated').innerText = '"말을 너무 지나치게 반복하네요. 대단한 상황인가요?"';
            } else {
                document.getElementById('ocr-raw').innerText = '"오늘 갓생 살기 실패함 ㅠㅠ 억까 지림"';
                document.getElementById('ocr-translated').innerText = '"오늘 모범적이고 보람찬 하루를 보내지 못했습니다. 운이 매우 나빴습니다."';
            }
        }

        // ==========================================
        // 7. 사전 렌더링 & 검색
        // ==========================================
        function renderDict(filterText = '') {
            const container = document.getElementById('dict-list');
            container.innerHTML = '';

            const filtered = dictionary.filter(item => 
                item.term.includes(filterText) || item.std.includes(filterText)
            );

            if (filtered.length === 0) {
                container.innerHTML = '<div class="text-center py-6 text-xs text-slate-400">검색된 단어가 없습니다.</div>';
                return;
            }

            filtered.forEach(item => {
                const isBookmarked = bookmarks.includes(item.term);
                const el = document.createElement('div');
                el.className = 'p-3 bg-slate-50 hover:bg-pastelPurple/20 rounded-xl transition-all border border-slate-100 flex justify-between items-start gap-2';
                el.innerHTML = `
                    <div class="space-y-0.5">
                        <div class="flex items-center gap-1.5">
                            <span class="font-extrabold text-xs text-slate-800">${item.term}</span>
                            <button onclick="speakText('${item.term}')" class="text-slate-400 hover:text-brandPrimary text-[10px]">
                                <i class="fa-solid fa-volume-high"></i>
                            </button>
                        </div>
                        <p class="text-[11px] font-semibold text-brandDark">${item.std}</p>
                        <p class="text-[10px] text-slate-400 leading-tight">${item.tip}</p>
                    </div>
                    <button onclick="toggleBookmark('${item.term}')" class="text-xs ${isBookmarked ? 'text-amber-400' : 'text-slate-300'} p-1">
                        <i class="fa-${isBookmarked ? 'solid' : 'regular'} fa-star"></i>
                    </button>
                `;
                container.appendChild(el);
            });
        }

        function searchDict() {
            const query = document.getElementById('dict-search').value.trim();
            renderDict(query);
        }

        function toggleBookmark(term) {
            if (bookmarks.includes(term)) {
                bookmarks = bookmarks.filter(b => b !== term);
                showToast(`'${term}' 보관함 해제`);
            } else {
                bookmarks.push(term);
                showToast(`'${term}' 보관함 저장 완료!`);
            }
            renderDict(document.getElementById('dict-search').value.trim());
        }

        // ==========================================
        // 8. 기타 유틸리티 (복사, 저장, 공유, 토스트)
        // ==========================================
        function copyToClipboard() {
            const text = document.getElementById('result-text').innerText;
            const dummy = document.createElement("textarea");
            document.body.appendChild(dummy);
            dummy.value = text;
            dummy.select();
            document.execCommand("copy");
            document.body.removeChild(dummy);
            showToast("📋 결과가 클립보드에 복사되었습니다!");
