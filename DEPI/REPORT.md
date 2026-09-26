# تقرير التدريب العملي | Internship training report

**الاسم:** أحمد محمد سعد الدين القصراوي  
**القسم:** الذكاء الاصطناعي — المستوى الثالث  
**الجهة:** مبادرة رواد مصر الرقمية - مايكروسوفت داتا سينس (شركه Eyouth)  
**مدة التدريب:** 120 ساعة

### تجربة التدريب والموضوعات التي درستها

درست خلال فترة التدريب تعلّم الآلة ومعالجة اللغات الطبيعية والتعلّم العميق من خلال شرح نظري وتطبيقات عملية. اتبع التدريب المراحل المعتادة لمشروع الذكاء الاصطناعي، بداية من تجهيز البيانات واختيار النموذج المناسب، ثم التدريب والتقييم، ووصولًا إلى إتاحة النموذج من خلال تطبيق يمكن استخدامه.

في تعلّم الآلة، درست تحويل البيانات الفئوية إلى أرقام باستخدام Label Encoding وOne-Hot Encoding، وتعلمت سبب الحاجة إلى Normalization أو Standardization قبل استخدام النماذج التي تعتمد على المسافات. شملت خوارزميات التصنيف Logistic Regression وK-Nearest Neighbors وSupport Vector Machines وDecision Trees وNaive Bayes. كما درست طرق Ensemble، ومنها Bagging وRandom Forest وAdaBoost وGradient Boosting وXGBoost. وتدربت على تقييم النماذج باستخدام Confusion Matrix وAccuracy وPrecision وRecall وF1-score وROC وAUC، مع فهم سبب عدم كفاية Accuracy وحدها عند التعامل مع فئات غير متوازنة. أما التعلّم غير الموجّه فشمل K-Means وDBSCAN، واستخدمت PCA لفهم تقليل الأبعاد والمشكلات الناتجة عن زيادة عدد الخصائص.

بدأ جزء معالجة اللغات الطبيعية بجمع النصوص وتنظيفها، واستخدام Regular Expressions، وتقسيم النص وتجهيزه للنموذج. قارنت بين Bag of Words وN-grams وTF-IDF وOne-Hot Representations وWord Embeddings مثل Word2Vec. بعد ذلك درست النماذج المتسلسلة، وكيف تحتفظ RNN وLSTM بمعلومات من الكلمات السابقة. كما تناول التدريب نماذج Encoder-Decoder وSeq2Seq للترجمة الآلية، ومشكلة ضغط الجملة الطويلة داخل تمثيل ثابت، وBeam Search، وآلية Attention.

في التعلّم العميق، تعلمت كيف تتكوّن الشبكة العصبية من الخلايا والأوزان والانحياز ودوال التنشيط. تابعت عملية التدريب بداية من Forward Propagation وحساب الخطأ، ثم Backpropagation وGradient Descent. شمل التدريب أيضًا مشكلة Vanishing Gradients وOverfitting وDropout وL1 وL2 Regularization، إلى جانب Optimizers مثل Momentum وAdam. ومن خلال Transfer Learning، تعلمت إعادة استخدام نموذج مدرّب مسبقًا، وتجميد الطبقات الأولى، وضبط الطبقات الأخيرة، واستخدام Early Stopping وModel Checkpoints. وبجانب هذه الموضوعات، تدربت على Git وGitHub وتتبع الأخطاء وقراءة الوثائق التقنية وواجهات البرمجة وقواعد البيانات وDocker وCI/CD والنشر على Microsoft Azure.

علمتني التطبيقات العملية مقارنة الطرق المختلفة بدلًا من التعامل مع كل خوارزمية كمعادلة منفصلة. أصبحت أسأل أولًا هل البيانات متوازنة، وهل تحتاج إلى Scaling، وهل ترتيبها مهم، وهل تحتوي على عدد كبير من الأبعاد. واستخدمت نتائج التدريب والتحقق لاكتشاف Underfitting أو Overfitting، ثم تعديل الخصائص أو Regularization أو Hyperparameters وفقًا للمشكلة. أفادني هذا الأسلوب لاحقًا عند تحليل سلوك وكيل DataPilot.

### نظرة عامة على مشروع DataPilot AI

كان المشروع الأساسي الذي عملت عليه هو [DataPilot AI](https://github.com/Omarnagyafifi1/datapilot-ai)، وهو تطبيق ثنائي اللغة من نوع Text-to-SQL. يسمح التطبيق للمستخدم بطرح سؤال عن قاعدة البيانات بالعربية أو الإنجليزية دون كتابة SQL. يمكن للمستخدم، على سبيل المثال، أن يسأل عن إجمالي المبيعات في شهر محدد. يفهم النظام الطلب، وينشئ الاستعلام، وينفذه على مصدر البيانات المختار، ثم يعرض النتيجة مع تفسير مختصر ورسم بياني عندما تكون البيانات مناسبة لذلك.

يدعم DataPilot قواعد SQLite وPostgreSQL وMySQL وSQL Server وOracle. ويمكنه أيضًا استيراد ملفات CSV وإتاحتها للاستعلام من خلال الواجهة نفسها. كُتبت الواجهة الخلفية باستخدام Python وFastAPI، بينما تعتمد الواجهة الأمامية على React وVite وTailwind CSS.

### دوري في المشروع

تركزت مسؤوليتي الأساسية على تصميم بنية وكيل الذكاء الاصطناعي، والأدوات التي يستطيع استخدامها، وطريقة تنسيق عمل هذه الأدوات. استخدمت LangGraph لتنظيم الوكيل في صورة State Graph بدلًا من معالجة الطلب كله داخل استدعاء واحد للنموذج. تحمل الحالة بين الخطوات سؤال المستخدم ونوع الطلب ومصدر البيانات ومخطط القاعدة واستعلام SQL والنتيجة وعدد محاولات التصحيح والأخطاء والتفسيرات والرسم البياني والأسئلة المقترحة.

تبدأ العملية بتحديد نوع الطلب: قراءة أو إضافة أو تحديث أو حذف. تمر أسئلة القراءة الواضحة من مسار سريع يعتمد على قواعد بسيطة، بينما يستخدم النظام النموذج اللغوي لتصنيف الأسئلة الأقل وضوحًا. بعد ذلك يقرأ الوكيل مخطط قاعدة البيانات ويختار الجداول والأعمدة المرتبطة بالسؤال. يقلل ذلك حجم النص المرسل إلى النموذج ويساعده على إنشاء استعلام أكثر ارتباطًا بالطلب.

عملت على الأدوات الخاصة بقراءة المخطط وإنشاء SQL وتنفيذ الاستعلام والتحقق من النتيجة وتصحيح الأخطاء وطلب الموافقة البشرية. في أسئلة القراءة، يستطيع الوكيل البحث في ذاكرة السيناريوهات عن سؤال مشابه وإعادة استخدام نمط SQL نجح سابقًا. إذا لم يجد نتيجة مناسبة، ينشئ استعلامًا جديدًا. وعند فشل التنفيذ، تُرسل رسالة الخطأ إلى أداة التصحيح، ويمكن للوكيل إعادة المحاولة حتى ثلاث مرات. أما طلبات تعديل البيانات فتسلك مسارًا منفصلًا وتتوقف إلى أن يوافق المستخدم على الاستعلام المقترح.

بعد نجاح التنفيذ، يجهز التطبيق ثلاثة مخرجات: مواصفات رسم بياني باستخدام Plotly، وتفسيرات بالعربية والإنجليزية، وأسئلة متابعة مقترحة. تعمل هذه المهام بالتوازي حتى لا ينتظر المستخدم انتهاء كل مهمة قبل بدء المهمة التالية. بعد ذلك تُحفظ النتيجة النهائية والاستعلام والرسم والتفسير في سجل الاستعلامات.

### زمن الاستجابة ومشكلات الوكيل

كان زمن استجابة الوكيل واعتماديته هو تخصصي التقني الرئيسي في DataPilot. قد يمر الطلب بمراحل تحديد النوع وقراءة المخطط والبحث في الذاكرة وإنشاء SQL والتنفيذ والتصحيح والرسم والتفسير واقتراح الأسئلة والتقييم. يضيف كل استدعاء للنموذج أو محاولة تصحيح وقتًا جديدًا، لذلك تتبعت زمن كل مرحلة على حدة بدلًا من التعامل مع زمن الاستجابة كرقم واحد.

وجدت عدة أسباب يمكن أن تجعل الوكيل أبطأ. يزيد مخطط قاعدة البيانات الكبير من حجم Prompt ووقت معالجة النموذج. كما تضيف استدعاءات LLM المتكررة تأخيرًا في الشبكة، وقد تصل إلى حدود الاستخدام الخاصة بمزوّد النموذج. ويمكن أن يؤدي فشل الاستعلام إلى دورات إضافية من الإنشاء والتنفيذ. كان المشروع يستخدم أيضًا طريقتين للذاكرة قد ترسلان معلومات مكررة، بينما احتاجت نتائج الاستعلامات المخزنة مؤقتًا إلى إبطال دقيق بعد تعديل البيانات. حسّن الانتقال إلى مزوّد بديل من توافر الخدمة، لكنه قد يزيد زمن الاستجابة إذا فشل المزوّد الأول.

استخدمت البنية عدة طرق لتقليل هذا التأخير. حُفظت نتائج قراءة المخطط مؤقتًا، وجرت تصفية المخططات الكبيرة قبل إنشاء SQL. عالج المسار السريع أسئلة القراءة البسيطة من دون استدعاء كامل لتصنيف النية. وسمحت ذاكرة السيناريوهات بإعادة استخدام حل سابق عندما كان السؤال الجديد مشابهًا بدرجة كافية. كذلك عملت مهام ما بعد التنفيذ بالتوازي، ووُضع حد لعدد محاولات التصحيح. تابعت مقاييس مثل متوسط زمن الاستجابة ونسبة النجاح وعدد النتائج ونسبة إنشاء الرسوم، حتى أعرف هل حسّن التعديل مسار العمل كاملًا أم عقدة واحدة فقط.

كشف العمل أيضًا عن نقاط تحتاج إلى تطوير لاحق. لم تكن طبقة الانتقال بين مزوّدي النماذج تحتوي على Timeout أو Circuit Breaker، وكان من الممكن أن تتجاوز المخططات الكبيرة عدد Tokens المتاح. كما أن Query Cache لم يستخدم سياسة LRU حقيقية أو مدة صلاحية TTL. واعتمد التعامل مع الأسئلة العربية بصورة أساسية على تعليمات داخل Prompt، لذلك كانت الأسئلة العربية المعقدة أصعب من الأسئلة الإنجليزية. أوضحت لي هذه المشكلات أن صحة SQL وحدها لا تكفي، وأن الوكيل يحتاج إلى هندسة دقيقة للسرعة والحالة والذاكرة المؤقتة واستعادة العمل بعد الفشل والمراقبة.

### الأمان والتقييم والنشر

لأن DataPilot ينفذ SQL أنشأه النموذج، كان الأمان جزءًا من مسار الوكيل. يمنع النظام أوامر خطرة مثل `DROP` و`ALTER` و`TRUNCATE`. أما الاستعلامات التي تغيّر البيانات، ومنها `INSERT` و`UPDATE` و`DELETE`، فتحتاج إلى موافقة المستخدم. تُشفّر بيانات الاتصال بقواعد البيانات قبل حفظها، كما يوجد حد لعدد الصفوف التي يعيدها استعلام القراءة لتجنب النتائج الكبيرة بصورة غير متوقعة.

يسجل المشروع نجاح الاستعلام وزمنه، ويقيّم SQL الناتج من حيث صحة الصياغة ودقة الإجابة واكتمالها وكفاءة الاستعلام واستخدام مخطط قاعدة البيانات. راجعت أيضًا أسلوب Execution Match المستخدم في الاختبارات، حيث ينفذ النظام الاستعلام الناتج والاستعلام المتوقع على قاعدة البيانات نفسها ثم يقارن النتائج. كانت هذه الطريقة أدق من مقارنة نص SQL فقط؛ لأن استعلامين مختلفين قد يعيدان الإجابة الصحيحة نفسها.

شاركت في إعداد النشر من خلال وضع التطبيق داخل Docker ونشره على Azure Container Apps. يحتفظ Azure Container Registry بصورة الحاوية، وتدعم Azure Database for PostgreSQL البيانات الدائمة، بينما تحفظ خدمات Azure Storage الملفات المرفوعة. وتتولى GitHub Actions بناء نسخة جديدة ونشرها عند إرسال تعديلات إلى فرع النشر. ربطت هذه المرحلة عملي على بنية الوكيل وزمن استجابته بسلوك النظام بعد تشغيله في البيئة السحابية.

---

**Name:** Ahmed Mohammed Saad ElDeen ELKassrawy  
**Department:** Artificial Intelligence — Level 3  
**Organization:** DEPI  Microsoft Data Science Track (Eyouth)
**Internship duration:** 120 hours

### Internship experience and topics studied

During my internship, I studied Machine Learning, Natural Language Processing, and Deep Learning through a mixture of theory and practical exercises. The training followed the usual life cycle of an AI project: preparing data, choosing a suitable model, training it, evaluating the result, and making it available through an application.

In Machine Learning, I learned how categorical data is converted into numbers using label encoding and one-hot encoding, and why normalization or standardization is needed before using distance-based models. I studied classification algorithms such as Logistic Regression, K-Nearest Neighbors, Support Vector Machines, Decision Trees, and Naive Bayes. I also worked with ensemble methods, including bagging, Random Forest, AdaBoost, Gradient Boosting, and XGBoost. Model evaluation covered the confusion matrix, accuracy, precision, recall, F1-score, ROC curves, and AUC, with attention to why accuracy alone can be misleading when classes are imbalanced. The unsupervised learning topics included K-Means and DBSCAN clustering, while PCA was used to understand dimensionality reduction and the problems caused by high-dimensional data.

The NLP part began with collecting and cleaning text, regular expressions, tokenization, and preparing text for a model. I compared Bag of Words, N-grams, TF-IDF, one-hot representations, and word embeddings such as Word2Vec. Later sessions covered sequence models and the way RNNs and LSTMs retain information from earlier words. I also studied encoder-decoder and Seq2Seq models for machine translation, the information bottleneck in long sequences, beam search, and the attention mechanism.

In Deep Learning, I learned how artificial neurons, weights, bias, and activation functions form a neural network. I followed the training process through forward propagation, loss calculation, backpropagation, and gradient descent. The course also covered vanishing gradients, overfitting, dropout, L1 and L2 regularization, and optimizers such as Momentum and Adam. Transfer learning showed me how to reuse a pretrained model, freeze early layers, fine-tune later layers, and use early stopping or model checkpoints. Alongside these topics, I practiced Git and GitHub, debugging, technical documentation, APIs, databases, Docker, CI/CD, and deployment on Microsoft Azure.

The practical sessions taught me to compare methods instead of treating each algorithm as a separate formula. I learned to ask whether the data was balanced, scaled, sequential, or high-dimensional before choosing a model. I used training and validation results to identify underfitting or overfitting and adjusted features, regularization, or hyperparameters accordingly. This way of thinking was useful later when I analyzed the behavior of the DataPilot agent.

### Project overview: DataPilot AI

The main project I worked on was [DataPilot AI](https://github.com/Omarnagyafifi1/datapilot-ai), a bilingual Text-to-SQL application. It allows a user to ask a database question in Arabic or English without writing SQL. For example, the user can ask for total sales in a particular month. The system interprets the request, generates a query, executes it against the selected data source, and returns the result with a short explanation and a chart when the data is suitable for visualization.

DataPilot supports SQLite, PostgreSQL, MySQL, SQL Server, and Oracle. It can also import CSV files and make them available for questioning through the same interface. The backend is written in Python with FastAPI, while the frontend uses React, Vite, and Tailwind CSS.

### My role in the project

My main responsibility was the architecture of the AI agent, the tools it could use, and the way those tools were coordinated. I used LangGraph to organize the agent as a state graph instead of handling the whole request in a single model call. The state carries the user's question, intent, selected data source, schema context, generated SQL, execution result, retry count, errors, insights, visualization, and suggestions from one step to the next.

The first stage routes the request into a read, add, update, or delete intent. Common read requests use a quick rule-based path, while less obvious requests are classified by the language model. The agent then reads the database schema and filters it to the tables and columns related to the question. This reduces the amount of context sent to the model and makes SQL generation more focused.

I worked on the tools used for schema inspection, SQL generation, query execution, validation, error correction, and human approval. For read requests, the agent can search its scenario memory for a similar question and reuse a successful SQL pattern. If there is no useful match, it generates a new query. When execution fails, the error is sent back to the correction tool, and the agent can retry up to three times. Requests that modify data follow a separate route and pause until the user approves the proposed query.

After a successful execution, the application prepares three outputs: a Plotly chart specification, bilingual insights, and suggested follow-up questions. These tasks run in parallel so the user does not have to wait for each one to finish in sequence. The final result, SQL, chart, and explanation are then stored in the query history.

### Latency and agent-related problems

Agent latency and reliability were my main technical specialty in DataPilot. A request may involve routing, schema loading, memory lookup, SQL generation, database execution, correction attempts, visualization, insights, suggestions, and evaluation. Each language-model call or retry adds time, so I traced the stages separately instead of treating the response time as one number.

Several issues could slow down the agent. A large database schema increases prompt size and model processing time. Repeated LLM calls add network delay and may reach provider rate limits. A failed query can trigger more generation and execution cycles. The project also had two memory mechanisms that could send duplicated context, and cached query results needed careful invalidation after database changes. Provider fallback improved availability, but switching providers could also increase latency when the first provider failed.

The architecture used several methods to reduce these delays. Schema results were cached, and large schemas were filtered before SQL generation. A fast router handled simple read questions without a full classification call. Scenario memory allowed the agent to reuse a previous solution when the new question was similar enough. Post-processing tasks ran in parallel, and retries were limited. I also followed operational measurements such as average latency, success rate, result count, and visualization rate to see whether a change improved the complete workflow rather than only one node.

The work also revealed areas that needed further improvement. The fallback model layer had no timeout or circuit breaker, large schemas could still exceed the available token budget, and the query cache did not have a true LRU policy or TTL. Arabic handling depended mainly on prompt instructions, which made complex Arabic questions more difficult than English ones. These problems taught me that an agent can generate correct SQL and still need careful engineering around speed, state, caching, failure recovery, and observability.

### Safety, evaluation, and deployment

Because DataPilot executes model-generated SQL, safety was part of the agent flow. Destructive commands such as `DROP`, `ALTER`, and `TRUNCATE` are blocked. Queries that change stored data, including `INSERT`, `UPDATE`, and `DELETE`, require user approval. Database credentials are encrypted before storage, and read queries have a result limit to prevent unexpectedly large responses.

The project records query success and latency and evaluates generated SQL for syntax, correctness, completeness, efficiency, and use of the database schema. I also reviewed the execution-match approach used in offline tests, where generated SQL and expected SQL are run against the same database and their results are compared. This was more useful than comparing the query text alone because two different SQL statements can return the same correct answer.

I worked with the deployment setup by packaging the application in Docker and deploying it to Azure Container Apps. Azure Container Registry stores the container image, Azure Database for PostgreSQL supports persistent data, and Azure storage keeps uploaded files. GitHub Actions builds and deploys a new version when code is pushed to the deployment branch. This connected my work on agent architecture and latency with the behavior of the system after deployment.
