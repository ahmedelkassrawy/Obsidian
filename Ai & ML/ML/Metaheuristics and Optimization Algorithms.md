### **First Page (Refined based on the "Case Study" slide)**

عندنا **50** عربية هتتوزع على 500 مدينة => عشان الـ agent والـ **Objective** هو الـ max/min والـ approach ده بينتهي بالـ climb process وهو الـ **local search** ممكن يفضل يطبقها لحد ما يكتشف حل بس لو كنا بنستعمل خوارزمي زي MA كان زمانه حالته هنا المميزة هي الـ **Somersault** بيكتشف الـ local traps فيحسب مسار أو route تاني خالص ويستكشف solution جديد والنتيجة انه بيتجاوز كل الزحمة وبيقلل 15% من المسافة الخاصة بيها.

---

### **Second Page (Refined based on the "Applications" & "Benchmark" slides)**

ليه بنفضل MA علشان قدرة الـ MA على البحث على local area في نفس ذات اللحظة اللي بيقع فيها في الخطأ من الـ traps وده بيطلعه منها بشكل كبير. بالنسبة للحياة الحقيقية أو الـ real world apps:

1. أولاً الـ تدريب للشبكات العصبية Neural Networks => بيستخدم الـ algo اننا نظبط الـ parameters, weights . كأن الـ algo بيقعد يدور في الـ graph لحد الـ best solution بـ **Somersault** process اللي اتأكدنا عليها انه يخرج أوزان التدريب من الـ **local minima** وده بيديني سرعة وكفاءة أكتر.
    
2. Power grid load balancing => الـ خوارزمية هنا بيمثل الـ dynamic manager بحيث بيوزع الـ حمل الكهربي في الـ real time عشان يقلل الخساير ويمنع حدوث أحمال زيادة على الشبكة.
    
3. **Traveling Salesperson Problem (TSP)** => بنستخدم فيها الخوارزمية عشان نقلل الـ **path** بين المدن.
    
4. الـ logistics and supply chain => بيتم التعامل مع طرق النقل وجعله محل اهتمام search space بمعنى ان الـ algo انه يكتشف millions combinations بحيث يحقق أقل تكلفة.
    

**MA > Particle Swarm Optimization > Genetic Algo > Artificial Bee Colony**

عشان اخلي الـ model يكتشف أول ما يشوف تلة صغيرة يقدر انه يكتشف انها الـ local minima => الـ particle swarm => يمشي ورا الأغلبية لو وقع كله بيقع وراه => الـ genetic => بيحاول يعوضه عن طريق الـ random mutation مع الـ Bee بيدرس مدى انه يكمل الـ لفة قدام أولا.

عشان كده بتكسب هنا علشان الـ climb process بيستكشف قمة التل => MA أسرع من الـ **Somersault** عكس العشوائية اللي كانت بتحصل احنا بنحسب نقطة الارتكاز وده بيخلينا نشوف أماكن جديدة غير مستكشفة.