from google import genai
import csv
import json
import os
import time
from datetime import datetime, date, timedelta
from difflib import get_close_matches

API_KEYS = [
    "AIzaSyCNDTDCSHbo0qE59rFpcINv-hhfVG99D_0", # Key 1
    "AIzaSyC7yCdiXkpfUO3EQso534b8GK2QA-smrWM",                  # Key 2
    "AIzaSyAwVv2Pctzr39wz8gkHth7qS5FqKYAWNW0"                   # Key 3
]
current_key_idx = 0
OUTPUT_FILE = "/home/jiclawdbot/Yeen/question_bank.json"
MINERVA_FILE = "/home/jiclawdbot/Yeen/minervaquestionsmerged.json"
SYLLABUS = """
Introduction to Medicine and Medical Science (IMMS).
Genetics: 
● DNA structure, function, packaging and replication 
● DNA transcription and translation 
● Purpose and stages of mitosis (and their microscopic appearance) 
● Purpose and stages of meiosis 
● Somatic and gonadal mosaicism 
● Gametogenesis 
● Mitotic abnormalities 
● Chromosome structure 
● Germline, somatic and mitochondrial genomes 
● Construction and interpretation of pedigrees 
● Karyotype interpretation (and examples) 
● Genetics terms and principles (as set out in glossary) 
● Phenotype vs. Genotype 
● Penetrance 
● Autosomal dominant inheritance (and examples of diseases) 
● Autosomal recessive inheritance (and examples of diseases) 
● Carrier and offspring risks 
● Consanguinity and its significance 
● X-linked inheritance (and examples of diseases) 
● X inactivation (Lyonisation) and its significance 
● Multifactorial and non-Mendelian inheritance 
● Genetic imprinting 
● Mitochondrial inheritance 
● DNA mutations (single nucleotide variants, copy number variants, loss of function variants and how they cause disease) 
● Genetic testing 
● Controversies surrounding genetic testing 
Cell biology: 
● Cell cycle 
● Molecular building blocks - sugars, nucleotides, amino acids, lipids 
● Protein structure (primary, secondary, tertiary, quaternary) 
● Sugars + glycosidic bonds 
● Peptide bonds 
● Enzyme function 
● Cell membrane ultrastructure and function 
● Membrane protein types 
● Movement across membranes (active and passive) 
● Cell membrane receptors, transport proteins and ion channels 
● Homeostasis 
● Autocrine, paracrine and endocrine cell signalling 
● Simple feedback loops (positive and negative feedback) 
● Overview of the endocrine system 
● Peptide and steroid hormones 
Energy metabolism / Biochemistry: 
● Basal metabolic rate - definition, calculation and factors affecting it 
● Dietary energy sources 
● Energy storage and excess 
● Prudent diet 
● ATP-ADP cycle 
● Aerobic and anaerobic glycolysis and how it is regulated 
● Krebs cycle and how it is regulated 
● Oxidative phosphorylation + electron transport chain 
● Fatty acid oxidation (beta oxidation) 
● Ketogenesis and when ketones are used 
● Water homeostasis and the distribution of body water 
● Plasma osmolality 
● Water excess and dehydration 
● Oncotic and hydrostatic pressure 
● Formation of effusions and oedema 
● Sodium homeostasis 
Embryo development from fertilisation to week 9: 
● Embryo development from fertilisation to week 4 
○ Blastocyst differentiation into embryoblast and trophoblast 
○ Development of the bilaminar and trilaminar disc 
○ Gastrulation and neurulation 
● Embryo development from weeks 4-9 
○ Embryo folding 
○ Formation of the primitive gut and body cavities 
○ Organogenesis 
Cell histology and their ultrastructural components: 
● Types of stains & their use/appearance 
● Cell ultrastructure - organelles, intracellular filaments 
● Epithelium types and where they can be found 
● Connective tissue types and their origins 
● Histology of adipose tissue, smooth muscle, fibrous and elastic connective tissue, cartilage 
● Types of collagen 
● Histology of elastic arteries, muscular arteries, arterioles, capillaries, venules, veins and lymphatics (and how to tell the difference) 
● Histology of peripheral nerves 
● Myelinated and unmyelinated axons 
● Schwann cells 
● Nodes of Ranvier 
● Synapses 
Introduction to anatomical features of the human body (note: most of the anatomy taught in this teaching block is revisited in the relevant block later in the year): 
● Anatomical position 
● Coronal, sagittal and transverse planes 
● Anatomical terminology 
● Musculoskeletal anatomy 
○ Axial and appendicular skeleton 
○ Joints, ligaments and tendons 
○ Movements and muscles 
● Nervous system 
○ Organisation of the nervous system 
○ Brain, brainstem and spinal cord 
○ Cerebral ventricles and cerebrospinal fluid 
○ Meninges 
○ Blood supply to the brain 
○ Autonomic nervous system (sympathetic, parasympathetic) 
○ Cranial nerves overview 
○ Spinal nerves overview 
○ Dermatomes and myotomes  
ILA 1 - Cystic Fibrosis
● The processes of transcription (DNA to mRNA) and translation (mRNA to protein), including the roles of mRNA, tRNA, and ribosomes. 
● The primary, secondary, tertiary, and quaternary structure of proteins, the bonds that hold them together, and how mutations can alter protein function. 
● The different types of DNA mutation, including the types of single nucleotide variants, and insertions or deletions, and how small nucleotide changes can affect protein function. 
● The type of DNA mutation that corresponds to the ΔF508 mutation which leads to cystic fibrosis, how this leads to abnormal CFTR protein function, and the main consequences of this. 
● Autosomal recessive, autosomal dominant, and X-linked inheritance patterns, including how CF is inherited. 
● Draw and interpret Punnett squares and pedigree diagrams using standard symbols.  
Cardiovascular system.
Principle features of haematology: 
● Constituents of blood (erythrocytes, leucocytes, platelets, plasma) 
● Function of plasma proteins 
● Coagulation cascade 
● ABO and Rhesus blood groups 
● Blood transfusions and their alternatives 
● Transfusion reactions 
● Platelet biochemistry, activation and function 
Physiological features of the cardiovascular system: 
● Electrical activation of the heart 
● Electrocardiogram (ECG) 
● Cardiac action potentials 
● Molecular mechanics of cardiac contraction 
● Cardiac cycle and the ECG 
● Diastole and systole 
● Mechanical events within the cardiac cycle 
● Frank-Starling law of the heart 
● How sympathetic and parasympathetic nervous systems affect the heart 
● Determinants of blood flow, blood pressure and cardiac output 
● Stroke volume 
● Ohm’s law 
● Pulse pressure 
● Poiseuille’s and blood flow 
● Blood pressure measurement 
● Mean arterial pressure 
● Local, neural, and hormonal vasodilators and vasoconstrictors 
● Baroreceptors and chemoreceptors, their location and how they function 
● Pulmonary vs. systemic circulation (e.g. blood pressure differences) 
Embryonic development of the heart and circulation: 
● Embryology of the heart and the circulation 
● Plan of the circulation 
● Vasculogenesis and angiogenesis 
● Embryonic aortic arch 
Histology of the cardiovascular system: 
● Cardiac muscle (and how it differs from smooth and skeletal muscle) 
● Endocardium, myocardium and pericardium 
● Cardiac conduction system 
● Cardiac valves 
● Constituents of blood 
● Erythrocytes 
● Leucocytes (neutrophils, eosinophils, basophils, lymphocytes, monocytes) 
● Platelets  
Anatomical features of the cardiovascular system: 
● Overview of anatomy of the thorax 
● Surface anatomy 
● Major thoracic structures on a normal chest-X-ray and CT of the thorax 
● Structure of the heart (internal and external) 
● Heart valves and papillary muscles 
● Heart surfaces and heart borders 
● Valve auscultation (location in relation to ribs, not sounds) 
● Coronary arteries and what they supply 
● Cardiac conduction system 
● Sympathetic nervous system and the anatomical basis of referred cardiac pain 
● Pericardium (structure, innervation) 
● Course of the vagus and phrenic nerves (in relation to the lung hila and diaphragm) 
● Branches of the aorta 
● Superior vena cava 
● Divisions of the mediastinum and their major contents 
● Cardiopulmonary circulation 
ILA 2 - Myocardial Infarction
● The major coronary arteries and their territories. 
● How coronary blood flow is supplied to the heart muscle and how it varies during the cardiac cycle. 
● The chambers, valves, and major vessels of the heart. 
● Pressure changes in each chamber during the cardiac cycle and when valves open and close. 
● Cardiac output (CO), stroke volume (SV), heart rate (HR) and total peripheral resistance (TPR), how they contribute to blood pressure (BP), and how they are regulated. 
● How blood pressure is controlled through neural and hormonal mechanisms, including the renin-angiotensin-aldosterone system (RAAS). 
● The electrical conduction system of the heart, including the SA node, AV node, bundle branches, and Purkinje fibres. 
● The phases of the cardiac action potential, including the movement of ions, and the concepts of depolarisation, repolarisation, and refractory periods. 
● The major modifiable and non-modifiable risk factors for cardiovascular disease. 
● Examples of lifestyle modifications, public health strategies, and screening in reducing cardiovascular disease. 
Respiratory system.  
Physiological features of the respiratory system: 
● Function of the upper airways 
○ Nose; external anatomy and vestibule 
○ Nasal turbinates and meatus 
○ Nasal functions 
○ Paranasal sinuses (frontal, maxillary, ethmoidal, sphenoidal) 
○ Pharynx; nasopharynx, oropharynx, [hypopharynx] 
○ Eustachian tubes and their role and anatomy 
○ Larynx; laryngeal functions, innervation, vagus nerve branches that are relevant 
○ Recurrent laryngeal nerve anatomy and function (left and right are different!) 
● General function of the lower airways; gas exchange 
○ Thoracic cage 
○ Rib articulation and movement 
○ Surface anatomy; angle of Louis (a.k.a. sternal angle), larynx 
○ Trachea, lung hilum 
○ Main and lobar bronchi 
○ Segmental branches 
○ Terminal bronchiole, acinus 
○ Respiratory bronchiole, the acinus 
○ Alveolar ducts, alveoli 
○ Pleura structure and function 
○ Diaphragm 
○ [Coronary Circulation] 
○ Lung circulations, bronchial and pulmonary 
○ Lung Innervation 
○ Airway tone 
■ Bronchoconstriction vs. dilation 
■ Nicotinic and muscarinic receptors 
■ Sympathetic and parasympathetic stimulation 
● Poiseuille’s law in relation to the airways 
● Lung Physiology 1 
○ Static lungs 
○ Rib movement and the respiratory pump 
○ Gas exchange, alveolar ventilation and alveolar perfusion 
○ CO2 elimination, oxygenation, alveolar gas equation, A-aDO2, oxygen-Hb dissociation curve 
○ Acid base [the lungs are important as acid base regulators] 
○ Arterial blood gases 
○ Respiratory acidosis 
● Lung Physiology 2 
○ Differences between pulmonary and systemic circulations 
○ Pulmonary haemodynamics 
○ Hypoxia versus hypoxaemia 
○ Causes of hypoxaemia 
○ Ascent 
○ Classification of diseases of the pulmonary circulation 
● Lung Physiology 3; measured physiology values 
○ Measurement of lung volumes 
○ Measured values in patients 
○ Forced expiration 
■ Volume Time 
■ Flow Volume 
■ Peak Expiratory Flow 
○ Transfer Estimates 
○ Exhaled nitric oxide (FENO) 
○ Oximetry for Sp02 measurement 
○ Arterial blood gases 
○ Predicted and abnormal values 
● Lung Physiology 4; control of breathing 
○ CO2 elimination 
○ Oxygenation 
○ Acid base control 
■ Henderson-Hasselbach equation 
■ Respiratory acidosis/alkalosis 
○ Respiration and control of breathing 
○ Input and output signals 
○ Breathing rhythm 
○ Central pattern generator 
○ Pontine and medullary respiratory sensory 
○ Mechanical and chemical receptors 
○ Respiratory drive 
○ Alveolar recruitment 
○ Inspiration and expiration 
○ Chemoreceptors (central and peripheral) 
○ Lung, airway and muscle receptors 
● Lung Physiology 5; respiratory failure 
○ Normal arterial blood gases (ABGs) 
○ Definitions used in respiratory failure 
○ Examples of type I and II respiratory failure 
○ Hypoxaemia 
○ Hypercapnia 
○ Oxygen treatment 
Immune features of the respiratory system: 
● Immune defence in the lung 
○ Mechanisms – innate vs. adaptive immunity 
○ Respiratory/alveolar epithelium 
○ Mucus composition 
● Acute inflammatory response 
● Role and functions of alveolar macrophages and neutrophils 
● Types of hypersensitivity and their characteristics (Gell and Coombs) 
● Cells involved in hypersensitivity and their roles 
● Effect of histamine in T1 reaction 
● Mechanism of anaphylaxis 
Lungs in wild environments 
● Units of gas and atmospheric pressure 
● Boyle’s Law [Dalton’s law, Henry’s law] 
● Diving with the lungs and dive types 
● Pulmonary Oxygen Toxicity 
● CNS toxicity 
● Gas leakage; pulmonary and vascular 
● Ascent and flying with the lung 
Genetic and environmental lung influences 
● Lung diseases with genetic components (e.g. asthma, cystic fibrosis, AATD, interstitial diseases) 
● Lung diseases with a significant work and hobby causation (asthma, hypersensitivity pneumonitis, COPD, interstitial lung disease, pleural disease, pleural mesothelioma, lung cancer) 
● Wider environmental considerations 
Allergy, hypersensitivity and the lung 
● Regulation of airway tone 
● Autonomic nervous system and the lung 
● Parasympathetic bronchoconstriction and sympathetic bronchodilation 
● Hypersensitivity 
● Type I, II, II and IV immune reactions 
First breath 
● How does the newborn baby survive? 
● Embryology 
● Physiology 
● Adaptive changes at birth 
● Physics 
● Laplace’s law and the importance of surfactant 
● Common abnormalities 
● Surfactant disease of the newborn 
Embryonic development of the respiratory system: 
● Respiratory diverticulum and lung buds 
● Foetal circulation and effect of first breath 
● Type 2 pneumocyte production and premature babies 
Histology of the respiratory system: 
● Respiratory and olfactory epithelium 
● Conducting airways 
● Vocal cords 
● Bronchi vs. bronchioles 
● Air-blood barrier 
● Clara cells 
● Type I and II pneumocytes 
● Alveoli 
● Pores of Kohn 
Anatomical features of the respiratory system / thorax: 
● Nasal cavity, paranasal sinuses and palate 
● Oral cavity, salivary glands and pharynx 
● Anatomy of the neck 
○ Bones and cartilages 
○ Major vessels and nerves 
○ Pharynx, larynx and thyroid gland 
● Surface anatomy of the thorax 
● Major thoracic structures on a normal chest-X-ray and CT of the thorax 
● Muscles of the pectoral region and thoracic wall 
● Thoracic cage 
● Pleura, lungs and bronchial tree 
● Pulmonary hila 
● Diaphragm and intercostal muscles (innervation, function, gross structure) 
● Breast (structure, vascular supply, lymphatic drainage) 
ILA 3 - Heart Failure
● The basic anatomy of the respiratory system, including the lungs, bronchial tree, pleura, and pulmonary circulation. 
● How stroke volume and cardiac output are regulated through end-diastolic volume/preload, afterload, and contractility. 
● The Frank-Starling mechanism and how it allows the heart to adapt to changes in blood volume, including the Frank-Starling curves. 
● How oxygen is transported in the blood. 
● The difference between the terms ventilation and perfusion, and how their relationship affects gas exchange. 
● The roles of hydrostatic and oncotic pressure in maintaining fluid balance, and which primary factors contribute to hydrostatic and oncotic pressure. 
● How the body detects and responds to a decrease in blood pressure. 
● The principles of DNACPR, including patient autonomy and best interests. 
ILA 4 - Chronic Obstructive Pulmonary Disease
● The gross anatomy of the lungs, bronchi, pleura, thoracic wall and diaphragm and their role in ventilation with regard to intrathoracic volume and pressure. 
● The accessory muscles of breathing, how they aid breathing, and their role in respiratory distress. 
● The process of gas exchange at the alveolar-capillary interface and the factors affecting oxygen diffusion. 
● How the body detects and responds to changes in levels of oxygen, carbon dioxide and pH in the blood including the location of the receptors and the subsequent changes in ventilation. 
● The different lung volumes and measurements calculated during spirometry. 
● Provide some examples of smoking cessation public health initiatives.  
Gastrointestinal tract and liver (GI-L).  
Physiological features of the gut: 
● Salivary gland structure, function and innervation 
● Swallowing mechanisms and reflexes 
● Gastric structure, secretion, motility and protective mechanisms  
● Digestion and absorption of macronutrients  
● Intestinal digestion, absorption and transport  
● Stages of defaecation 
Physiological features of the liver, gallbladder and pancreas: 
● Liver storage 
○ Fat soluble vitamins 
○ Vitamins and iron storage 
● Liver detoxification 
○ Xenobiotics (definition and examples) 
○ Phase 1 and phase 2 detoxification reactions 
○ Cytochrome P450 function 
● Production of protein 
○ Albumin – function, production, deficit 
○ Clotting factors 
○ Complement factors 
● Fat metabolism 
○ Energy reserves in the body 
○ Differences between white and brown fat 
○ Enzymes – lipoprotein lipase, hepatic lipase 
○ Beta oxidation 
● Nitrogen balance 
○ Urea cycle 
○ Glucose/alanine cycle 
● Gallbladder 
○ Production and contraction of bile 
○ Bilirubin and enterohepatic secretion of bile salts 
● Exocrine pancreas 
○ Phases of secretion 
○ Secretion of bicarbonate 
○ Control of secretion – stimulation and inhibition 
Embryonic development of the gastrointestinal tract and liver: 
● Division of foregut/midgut/hindgut and their innervation and vascular supply 
● Development of the foregut and derivatives 
● The stages of development of the midgut 
● Development of the hindgut 
Histology of the gastrointestinal tract and liver: 
● Histology of the gut tube 
● Mouth and salivary glands 
● Oesophagus 
● Stomach 
● Small and Large Intestine  
● Liver 
● Gallbladder 
● Bile ducts 
● Exocrine pancreas - acini and ducts 
Anatomical features of the gastrointestinal tract and liver, and abdomen: 
● Surface anatomy of the abdomen 
● Muscles of the anterior abdominal wall 
● Location, borders and superficial and deep rings of the inguinal canal 
● Blood supply to the gastrointestinal tract and abdominal organs 
● Innervation of the gastrointestinal tract (sympathetic and parasympathetic) and abdominal organs 
● Anatomical basis for patterns of referred pain from the abdominal viscera  
● Anatomy of the stomach 
● Anatomy of the duodenum 
● Anatomy of the small and large intestines and their differences 
● Peritoneum and retroperitoneal organs 
● Greater and lesser omentum 
● Gross anatomy of the liver, spleen and pancreas 
● Portal venous system 
● Anatomy of the gallbladder and biliary tree 
● Major abdominal structures on a normal abdominal X-ray and CT abdomen 
ILA 5 - Gastritis and Appendicitis
● The anatomy of the stomach, small intestine, and large intestine, including blood supply, relevant surface anatomy landmarks and the nine regions. 
● The location of the appendix and the associated structures that contribute to clinical signs in appendicitis including the peritoneum and abdominal wall. 
● The mechanisms by which the stomach produces acid and how this is regulated (including roles of gastrin, histamine, and acetylcholine). 
● How the gastric mucosa protects itself from acid. 
● The sympathetic innervation of the gut and how this contributes to the visceral pain and referred pain experienced in inflammation of the stomach, appendix and sigmoid colon. 
● The features that distinguish between visceral and somatic pain in the abdomen and explain how peritoneal involvement alters pain character and location. 
● Key histological features of the stomach, small intestine, and large intestine, and how they relate these to their functions in digestion and absorption. 
● Key statistical terms including prevalence, incidence, sensitivity, specificity, positive predictive value and negative predictive value in medical testing, and how to calculate them. 
Neuroscience.  
Neuroanatomy 
● Neuroanatomical terminology 
● Neuroembryology including neurulation, milestones in brain development and formation of the ventricles 
● Common disorders in neurodevelopment and their consequences 
● General features of the external aspect of the brain including the ventral surface 
● Somatotopic and proportional representation of the homunculus on the primary motor and primary somatosensory cortices (pre- and post-central gyri) 
● Anatomy of the cranial meninges 
● Anatomy and function of the blood-brain barrier 
● Anterior and posterior blood supply to the brain including the circle of Willis 
● Venous drainage of the brain and identify the dural venous sinuses 
● Parts of the ventricular system, and where the production and drainage of cerebrospinal fluid takes place 
● Functions of lobes, systems, gyri, structures and nuclei 
● Experimental designs in systems-level investigations 
○ Effects of experimental manipulations on brain structure/activity 
○ Effects of brain manipulations on behaviour/physiology/endocrinology 
○ Increasing levels of specificity afforded by different experimental procedures 
○ Concepts of methodological specificity can be used to critically evaluate experimental investigations 
● Histological types of human muscle 
● Muscle structure and function; innervation, fibre typing, muscle contraction 
● Pattern of innervation and fibre typing is altered in denervating disease 
● Mitochondrial cytopathies as examples of energy pathology 
● Dystrophinopathies as examples of disorders of sarcolemmal structure 
● Disorders of neuromuscular transmission 
● Histological structure of peripheral nerve 
● Pathological classification of types of peripheral nerve disease 
● Pathology of axonal degeneration and demyelination 
● Bones that make up the skull and the cranial fossae 
● Foramina in the base of the skull and know what passes through each of them 
● Contents of the bony orbit, including nerves, extraocular muscles, and eye anatomy 
● How different cranial nerves and extraocular muscles contribute to eye movements 
● How changes in the amount of light entering the eye causes changes in pupil diameter 
● Auditory conduction, auditory pathways and the vestibulo-cochlear system 
● Contents of the outer, middle, and inner ear cavities 
● Three parts of the brainstem, their gross anatomical features and functions 
● All 12 cranial nerves, the location of their nuclei, functions and where they enter / exit the brain and skull 
● How visual information is conveyed from the retina to the primary visual cortex and how disruptions to this pathway causes various visual field defects 
● Gross anatomy and functions of the cerebellum 
● Major cells of the cerebellar cortex 
● Midline structures of the brain visible on a midsagittal section 
● Functions and parts of the limbic system including Papez circuit 
● Parts and functions of the basal ganglia and the internal capsule  
● Underlying biochemical and anatomical defects in Parkinson's Disease and Huntington's Chorea 
● Processes underlying the control of movement 
● Projection, commissural and association fibre tracts 
● Anatomy of the vertebral column, including the features of each type of vertebrae 
● Intervertebral discs, ligaments and muscles that support the vertebral column 
● Anatomy of the spinal cord including the formation of spinal nerves 
● Ascending and descending spinal tracts, their courses, functions, and spatial locations 
● Neuroradiology, imaging modalities and planes of section 
● How the main cortical and deep brain structures appear on CT and MRI including the brainstem 
● Neurological, neurosurgical and neuropsychological clinical relevance of anatomy studied (this will not be examined in Phase 1, but provides context to the ‘normative systems’ content and is vital content for later Phases and your future clinical careers) 
Neurophysiology 
● Structure of different axons 
● Axonal sheath differences in CNS and PNS 
● Role of neuroglia (astrocytes, oligodendrocytes [Schwann cells], microglia and ependyma) 
● Excitatory, inhibitory and modulatory synapses 
● Structure of a ‘model’ neuron and be able to draw a labelled diagram 
● Resting potential and how it is established 
● Post-synaptic potentials 
● Action potential and how it is generated 
● Physiology of action potential transmission down axons 
● Role of myelin in action potential transmission 
● Dysfunctional axonal transmission explaining the symptoms of multiple sclerosis 
● Five fundamental processes required for neurotransmission 
● Major neurotransmission systems and know some of the drugs that influence them 
● Why making drugs for specific brain diseases is difficult 
● Physiology of pain 
● C and A delta nerve fibres 
● Substance P 
● Action of opioids 
● Pain pathways 
● Anaesthetics and analgesics 
● Periaqueductal grey 
● Melzack-Wall gate control theory of pain 
● Difference between upper and lower motor neurons 
● Autonomic nervous system structure and function 
● Systems and their components involved in control of movement (upper and lower motor neurons and extra pyramidal) 
● Features of upper motor, lower motor and extra pyramidal disorders 
● Organisation of the central motor pathway (supplementary motor area to muscle) 
Psychiatry and psychological & sociological principles in behavioural neuroscience 
● Importance of the brain in human behaviour and experience 
● Mind and brain and distinction and how this influences the way we think about neurology and psychiatry 
● Mind-body dualism 
● Biological, psychological and social correlates of schizophrenia 
● Neurobiology of perception 
● Definition, role, neurobiology and theories of emotion 
● Difference between sensation and perception 
● Bottom-up and top-down processing 
● Causes of hallucinations including mental illnesses 
● Relationship of the perceptual set and our experiences 
● Biopsychosocial approach of managing mental illness 
● Neurobiology of stress 
● Evolutionary influences on behaviour 
● Emotional drivers impacting behaviour 
● Definitions and current psychological understanding of pain and its expression (particularly chronic pain) 
● Biopsychosocial factors affecting pain generation and awareness 
● Common recommended approaches to manage pain 
● Role of ‘chemical imbalance’ in depression 
● Role of stress hormones and effect on brain plasticity 
● Functional neuroimaging findings in depression 
Neurohistology 
● Neuromuscular junction 
● Motor unit 
● Golgi tendon organs 
● Muscle spindle 
● Histology of neural tissue  
ILA 6 - Stroke
● The gross anatomy of the brain, including the major lobes, gyri, sulci and ventricles. 
● The arterial blood supply to the brain, with a focus on the cerebral arterial circle (circle of Willis) and the territories supplied by the anterior, middle, and posterior cerebral arteries. 
● The primary neurological functions carried out by each lobe of the brain. 
● The functional anatomy of the brain and how impaired blood flow through specific cerebral arteries causes certain symptoms and signs. 
● The structure and function of the meninges, including the names and locations of the compartments between each one (extradural, subdural and subarachnoid). 
● The four principles of medical ethics (autonomy, beneficence, non-maleficence, and justice) and how they apply to decision making. 
ILA 7 - Vestibular Schwannoma
● The twelve cranial nerves, their main functions and their points of origin from the brain or brainstem. 
● The basic function of the cerebellum. 
● How action potentials are generated and propagated along myelinated axons, including the roles of sodium and potassium ion channels. 
● The role of myelin and the nodes of Ranvier in saltatory conduction. 
● Synaptic transmission, including neurotransmitter release, receptor binding, and signal propagation across the synaptic cleft. 
● The hierarchy of evidence and basic study design of each type of study. 
● The key features of an RCT, including randomisation, blinding, control groups, and outcome measures. 
● Why RCTs are considered the gold standard for testing the effectiveness of interventions.
Skin, UroGenital, Endocrine and Reproduction (SUGER). 
Physiological features of the renal and urinary system: 
● Glomerular filtration rate 
● Filtration and pressures at the glomerulus 
● Filtration barrier (glomerular basement membrane) 
● Concepts of osmolality and osmolarity 
● Structure of a nephron (glomerulus and tubules) 
● Ion and water transport at the nephron 
● Hormones and their function: renin-angiotensin-aldosterone system (RAAS), parathyroid hormone, aldosterone, atrial natriuretic peptide (ANP), antidiuretic hormone (ADH)/vasopressin (AVP) 
● Metabolic and respiratory acidosis/alkalosis 
● Control of micturition (nerve supply to muscles in the bladder) 
● Mechanisms of urine voiding and storage 
● Erythropoietin 
Physiological features of the reproductive system: 
● Ovarian structure - including reserve of primordial follicles 
● Stages of follicle development and ovulation 
● Testicular structure and spermatogenesis  
● HPG axis and gonadal steroidogenesis 
● Menstrual cycle including uterine and cervical changes 
● Changes at menopause 
● Fertilisation, early embryonic development and implantation 
● Maternal physiological adaptations during pregnancy 
● Placental structure and function 
● Stages of labour and factors involved in initiation 
Physiological features of the endocrine system: 
● Negative and positive feedback loops 
● Differences between anterior and posterior pituitary gland 
● Axis of anterior and posterior pituitary gland (oxytocin, vasopressin, ACTH, TSH, LH, FSH, GH, prolactin) 
● Production of thyroid hormone 
● Differences between T3 and T4 
● Function of thyroxine 
● Parathyroid gland – structure, function 
● Cell types in islet of Langerhans 
● Function of insulin 
● Physiological response to high/low glucose 
● Mechanism of insulin secretion 
● Structure of adrenal gland and hormone production 
● Function of aldosterone, cortisol, adrenaline, noradrenaline 
● Hormone receptor locations, secondary messenger theory 
Physiological features of the skin: 
● Waterproof/physical barrier 
● Vitamin D synthesis 
● Endocrine organ 
● UV light barrier 
● Immune organ 
● Sensory organ 
● Thermoregulation 
Embryonic development of the urogenital and reproductive organs: 
● Importance of primordial germ cell migration for gonadal development 
● Mullerian and Wolffian ducts 
● Differentiation of the indifferent gonad and the fates of the mesonephric and paramesonephric ducts  
● Differentiation of the external genitalia  
● Development of the kidneys 
● Development of bladder and urethra 
Histology of SUGER, with a focus on: 
● Skin - epidermis, epidermal appendages, dermis, subcutis, breast, lactating breast 
● Male reproductive tract - testis, epididymis, spermatic cord, seminal vesicles, prostate, penis 
● Female reproductive tract - ovary, fallopian tube, endometrium (in each stage of menstrual cycle), myometrium, endocervix, transformation zone, ectocervix, vagina, vulva 
● Endocrine system - pituitary, pineal, thyroid, parathyroid, endocrine pancreas 
● Urinary tract - kidney, urothelium, ureter, bladder, urethra 
Anatomical features of the urogenital and pelvic organs: 
● Major bony landmarks and joints of the pelvis  
● Inguinal canal (borders and contents) 
● Anatomy of female genitalia and pelvic organs: vulva, erectile tissues, vagina, cervix, uterus and uterine tubes, ovaries, rectum. 
● Anatomy of male genitalia and pelvic organs: penis, erectile tissues, scrotum and testes, prostate, seminal vesicles and ejaculatory duct, and rectum. 
● Differences between the male and female urethra. 
● Blood supply to organs of the pelvis (overview, main arteries and veins only) 
● Anatomy of the kidney, ureters and adrenal glands, including vasculature 
● Anatomy of the posterior abdominal wall (muscles, large nerves, aorta and IVC). 
● Anatomy of the urogenital triangle (and structures). 
● Pelvic floor muscles. 
ILA 8 - Dehydration and Acute Kidney Injury
● The gross anatomy of the kidneys, ureters, bladder, and urethra of the male and female. 
● The microscopic structure of the nephron and the role of each part in urine formation. 
● The basic processes of glomerular filtration, tubular reabsorption, and secretion in the nephron. 
● How changes in the diameter of the afferent and efferent arterioles of the glomerulus affect glomerular filtration rate (GFR). 
● The main sites of reabsorption and secretion of water and key ions (sodium, potassium, hydrogen, and bicarbonate) within the nephron, including the proximal convoluted tubule (PCT), loop of Henle, distal convoluted tubule (DCT), and collecting ducts. 
● The hormonal regulation of water reabsorption, including the roles and mechanisms of aldosterone and antidiuretic hormone (ADH). 
○ The renal mechanisms involved in acid-base balance, particularly the reabsorption of bicarbonate and the secretion of hydrogen ions. 
ILA 9 - Subfertility
● The anatomy of the female reproductive tract, including the ovaries, uterine tubes, uterus, cervix, and vagina, including the structure and function of each part. 
● How the hypothalamic-pituitary-ovarian (HPO) axis regulates the menstrual cycle, including the roles of GnRH, FSH, LH, oestrogen, and progesterone. 
● How these hormones influence the ovaries, endometrium and cervix across the cycle. 
● The process of spermatogenesis, including the stages of sperm development, maturation, and storage. 
● Sperm structure and function in relation to fertilisation. 
● The physiological processes involved in fertilisation, including oocyte maturation and ovulation, sperm transport and capacitation and fertilisation. 
Musculoskeletal (MSK). 
Intro 
● MSK importance / health burden 
● Range of common MSK disorders  
Bone 
● Function of skeleton 
● Types of bone 
● Trabecular and cortical structure 
● Toughness/stiffness 
● Bone cell lineage and function 
● Modelling/remodelling 
● Types of collagen 
● Synthesis and structure 
● Bone matrix and mineralisation 
● Bone growth and life course 
● Bone turnover, coupling, balance 
● Hormonal control of bone 
● RANK/RANKL/OPG 
● Wnt and sclerostin 
● Why bones respond to loading 
● Stress and strain 
● Strains of different activities 
● Mechanostat and strain signalling 
● Basic mechanics of fractures 
● Describing fractures 
● Normal fracture healing 
Joints  
● Types of joint 
● Common characteristics  
● Directions of movement 
● Hip/shoulder/knee/elbow 
● Synovial cartilage and synovial membrane 
● Vertebrae and disc structure and function 
● Tendon and ligaments – similarities and differences 
● Loading and Golgi organs 
Muscle  
● Function of skeletal muscle 
● Universal characteristics 
● Muscle structure 
● Physiology of contraction 
● Neuromuscular junction 
● Fibre types 
● Energy cycling 
Exercise 
● Measuring fitness 
● Obesity 
● Cardiorespiratory fitness and mortality 
● Physical activity effects on health 
● Activity guidelines and interventions 
Biochemistry/homeostasis  
● Calcium  
o Diet and gut absorption 
o Renal handling 
o Actions of PTH 
o Vit D synthesis and action 
o Calcitonin 
● Phosphate 
o Roles of phosphate in biology 
o Diet and gut absorption 
o Renal handling 
o Bone mineralisation 
o PTH and FGF23 
● Purines and uric acid 
o Uric acid sources 
o Uric acid metabolism 
o Causes of high uric acid 
o Gout, Lesch-Nyhan 
Histology: 
● Skeletal muscle (and differences between skeletal, smooth and cardiac muscle) 
● Bone histology 
● Ossification 
● Cartilage 
ILA 10 - Distal Radius Fracture
● The anatomy of the upper limb, including the bones, and key nerves and arteries. 
● The microscopic structure of bone tissue, including cortical and trabecular bone. 
● The cellular components of bone (osteoblasts, osteocytes, osteoclasts) and their roles in bone formation, maintenance, and remodeling. 
● The regulation of calcium homeostasis in the body, including the roles of parathyroid hormone (PTH), calcitonin, and vitamin D. 
● How these hormones affect bone metabolism, intestinal calcium absorption, and renal calcium handling. 
● The importance of patient confidentiality in healthcare settings. 
● The principles of medical privacy, when information can be shared, and the professional responsibilities of healthcare workers in protecting patient information.
Themes 
Prescribing.  
Use of FP10 prescriptions in Primary Care (linked to ‘Generalism and holistic patient care’ - EYGP session 1) 
● FP10 prescriptions 
● Minimum requirements to produce a valid and legal prescription 
● How patients may pay for their prescriptions 
● Abbreviations that may be used on prescriptions 
Legal restrictions around prescribing (linked to ‘Pregnancy’ - EYGP session 2) 
● Difference between a drug and a medicine 
● Which healthcare professionals are able to prescribe 
● Legal classifications of medicines (GSL, P and POM) and how each can be obtained by a patient 
Routes of drug administration and medicine formulations (linked to ‘Ischaemic heart disease / Health inequalities’ - EYGP session 3) 
● Different routes of drug administration 
● Local and systemic drug administration 
● Formulation of medicines for different routes of administration 
Sustainable prescribing (linked to ‘Asthma / Sustainable healthcare’ - EYGP session 4) 
● How the prescribing of medicines can negatively impact the environment 
● Steps that can be taken to reduce the environmental impact of medicines use 
Non-pharmacological interventions (linked to ‘Irritable bowel syndrome (IBS) / Functional disorders’ - EYGP session 5) 
● Non-pharmacological treatment options 
● Benefits of non-pharmacological treatment options 
● Barriers to non-pharmacological treatment options 
Prescribing Controlled Drugs (linked to ‘Neurodiversity’ - EYGP session 6) 
● Legal classification of controlled drugs (Schedule 1 to 5) 
● Why drugs may be classified as a CD 
● Prescription requirements for schedule 2 and 3 CDs 
National processes for medicines management (linked to ‘Epilepsy’ - EYGP session 7) 
● Role of the MHRA and NICE in making newly developed medicines available for prescribing on the NHS 
● Role of local drug formularies 
Communication and patient counselling (linked to ‘Skin / Fitness to practice’ - EYGP session 8) 
● Where patients might access information about their medicines 
● What a patient should be made aware of when starting a new medicine 
● Different methods for providing information to patients about their medicines 
Adherence and non-adherence (linked to ‘Chronic kidney disease (CKD) / Accessing healthcare for non-English speaking populations’ - EYGP session 9) 
● Issue of poor medicines adherence 
● Reasons for poor medicines adherence 
● Consequences of poor adherence 
● Strategies for preventing poor adherence 
Medicines supply chain (linked to ‘Menopause’ - EYGP session 10) 
● Medicines supply chain 
● What causes widespread drug shortages 
● Impact of drug shortages on patients and the healthcare system 
Drugs associated with dependence and withdrawal symptoms (linked to ‘Osteoarthritis / Chronic pain - EYGP session 11) 
● Types of medicines associated with dependence or withdrawal symptoms 
● Risks associated with strong opiates in chronic pain 
● Drug classes associated with increased risk of dependence or harm 
● Steps that prescribers can take to reduce risk of harm if prescribing a drug which can cause dependence 
Public health. 
Prevent disease and promote good health: 
● Public health focuses on the health of populations, not just individuals. This perspective allows you to understand the many factors that influence the health of populations, and strategies for disease prevention and health promotion. 
Address social determinants of health: 
● Public health emphasises the social, economic, and environmental factors that contribute to health disparities. This knowledge can be used to address the underlying causes of diseases and improve health outcomes for vulnerable populations. 
● A good understanding of public health will allow you to learn to advocate for policies and programs that promote health equity and address the social determinants of health. 
Deliver effective and efficient healthcare: 
● Public health principles help you understand the importance of equitable and efficient resource allocation and the need to balance individual needs with the needs of the population. 
● Knowledge of public health can inform the development of quality improvement initiatives and help contribute to improving the overall quality of healthcare. 
Take an interdisciplinary approach: 
● Public health requires collaboration with a variety of professionals, including [but not limited to] statisticians, epidemiologists, psychologists, sociologists, healthcare management. Understanding public health principles fosters effective collaboration to address complex health issues. 
Three pillars of public health 
● Health protection 
● Health services 
● Health improvement 
Public health in practice – application of the principles of public health 
● Principles of Evidence Based Medicine 
● Health inequities, and access to healthcare for vulnerable populations [older adults, migrants, patients with learning disabilities] 
● Key issues and considerations of NHS screening programmes 
● Key issues around reproductive and sexual health 
● Economic evaluation in health care 
● Impact of globalisation and environmental health on human health 
Medical sociology 
● Social and medical models of health and illness 
● Sick role: norms, deviance, and stigma 
● Role of medicine in society 
Behaviour and society 
● Common issues and implications of health-related reporting by the media 
● Key public health challenges: including smoking and obesity 
● Individual and population approaches to behaviour change 
● The use of complementary and alternative therapies, why patients use them, and how this might affect the safety of other types of treatment that patients receive 
Public mental health 
● Role of stress in health and illness 
● Psychological aspects of pain and pain management 
Common Mental Health Disorders (CMDs): prevalence, impact, and management 
Critical numbers. 
Quantitative study design 
● Populations and samples 
● Bias and confounding 
● Association vs. causation 
● Types of study design, including: 
○ Randomised controlled trials 
○ Cohort studies 
○ Case-control studies 
○ Cross-sectional studies 
● Hierarchy of evidence 
Summary statistics 
● Types of data 
● Summary statistics for categorical data 
● Summary statistics for numeric data 
● Quantifying associations and between-group differences 
Inferential statistics 
● Sampling variation 
● Hypothesis testing 
● Estimation-based inference 
● How to interpret and communicate results: 
○ Point and interval estimates 
○ Probability values 
○ Statistical significance vs. clinical importance 
○ Clinical risk prediction 
Critical appraisal 
● How to review and evaluate the quality of evidence 
● Use of critical appraisal tools 
Early Years General Practice (EYGP).
Session 1 ‘Generalism and holistic patient care’ (during IMMS block) 
● Role of a general practitioner and differences between primary and secondary care. 
● ‘Person centred care’ and examples of how this may look in practice. 
● Correct handwashing technique. 
● Giving constructive feedback to a colleague. 
Session 2 ‘Pregnancy’ (during IMMS block) 
● Factors (e.g. past medical history, family history) which would make a pregnancy ‘higher risk’, and explain measures used to reduce these risks if available. 
● Dietary and lifestyle advice to a pregnant woman. 
● Routine antenatal care in the UK, including what happens in a routine midwife appointment and what scans / blood tests are routinely offered. 
○ Additional tests offered to screen for and diagnose foetal genetic abnormalities. 
● Domestic abuse, possible risk factors / indicators, and the HARK screening tool. 
Session 3 ‘Ischaemic heart disease / Health inequalities’ (during Cardiovascular block) 
● Principles of primary and secondary prevention, particularly in relation to cardiovascular disease 
● Qrisk3 score and its use in the primary prevention of CVD. 
● Modifiable and non-modifiable risk factors for ischaemic heart disease 
● Lifestyle advice to a patient to reduce their risk. 
● Radial pulse and measure blood pressure with a manual sphygmomanometer. 
● Investigations (including blood tests and imaging) used to assess cardiac / chest pain and why. 
● Social inequalities impacting cardiovascular health in the UK. 
Session 4 ‘Asthma / Sustainable healthcare’ (during Respiratory block) 
● Diagnosis of asthma, and how to use an inhaler/ spacer device. 
● Communication skills required when consulting with a child or adolescent / with a parent in the room. 
● Different types of inhalers available and the pros and cons of each - particularly focusing on the environmental impact of different treatment options. 
● Socio-economic, environmental and cultural factors that impact the prevalence and incidence of childhood asthma. 
Session 5 ‘Irritable bowel syndrome (IBS) / Functional disorders’ (during GI-Liver block) 
● Differential diagnosis for diarrhoea, and identify important questions to ask to narrow this down. 
● Appropriate investigations for diarrhoea (stool, blood, imaging), and give directions to a patient for how to take a stool sample. 
● What a ‘functional illness’ is, and be able to explain the diagnosis of Irritable Bowel Syndrome to a patient without using any medical jargon. 
● Basic management of Irritable Bowel Syndrome, including lifestyle, diet and medications used. 
● Stigma surrounding functional illnesses such as chronic fatigue syndrome, fibromyalgia, and the impact of persistent physical symptoms on a patient’s quality of life / mental health. 
Session 6 ‘Neurodiversity’ (during Neurosciences block) 
● The ways in which neurodiversity (specifically ADHD and autism) may present and how these may differ according to age and gender. 
● How neurodiversity traits may affect a patient and/ or their family. (e.g. school life, employment, relationships, social interactions etc.) 
● Different approaches for consulting with autistic patients, including adapting communication style and the physical environment. 
● The support services available for neurodivergent (ND) individuals/families in South Yorkshire/North Derbyshire. 
● Treatment options for ADHD. 
Session 7 ‘Epilepsy’ (during Neurosciences block) 
● Differential diagnosis for falls and identify key features in the history which will help to narrow this down. 
● How a diagnosis of epilepsy may impact on the practicalities of a patient’s life (e.g. driving, employment, family planning, social activities). 
● How epilepsy is perceived in different cultures, the stigma that can be associated with epilepsy, and the behavioural/ mental health consequences of receiving a diagnosis. 
Session 8 ‘Skin / Fitness to practice’ (during SUGER block) 
● A list of important questions to ask a patient who presents with probable eczema, including symptoms, risk factors, exacerbating factors and psychosocial impact. 
● Basic pathophysiology of eczema to a patient without using jargon, and describe how to apply topical treatments correctly (and in the correct quantities). 
● How skin conditions present differently for patients with different skin colours, with particular focus on how eczema presents in black and brown skin. 
● Ethical/medico legal issues around self-prescribing and prescribing for friends and family. 
● When, where and why medical professionals should seek help for ill health (with reference to the GMC ‘fitness to practice’ guidance). 
Session 9 ‘Chronic kidney disease (CKD) / Accessing healthcare for non-English speaking populations.’ (during SUGER block) 
● Risk factors for developing CKD and list relevant investigations used when diagnosing and monitoring the condition. 
● Management options for end stage renal failure including different types of renal replacement therapy. Use a person centred approach to deciding which option may be best for a particular patient. 
● Different options available for translating in health care settings and the pros and cons of each. 
● Barriers to healthcare that may exist for patients where English is not their first language, and consider strategies to help patients from minority ethnic groups engage more with healthcare services. 
Session 10 ‘Menopause’ (during SUGER block) 
● Menopause and perimenopause, and list the various symptoms that a (peri-) menopausal patient may experience (e.g. vasomotor, genitourinary, psychological). 
● Impact that menopause may have on a patient from a personal, social and economic perspective. 
● How ethnicity can affect menopause and its management. 
● Risks and benefits of HRT, and identify contraindications to starting systemic treatment. 
● Types of HRT available, the modes of delivery, and why one method might be chosen over another. 
Session 11 ‘Osteoarthritis / Chronic pain’ (during MSK block) 
● WHO pain ladder, and the main side effects of different analgesic options. Counsel a patient regarding the side effects of long term opioid use. (You may wish to combine this objective with the one above or below, and include another learning objective selected by the group) 
● Counsel a patient regarding treatment of chronic pain (i.e. without long term opioids) and offer suggestions for non-pharmacological approaches to pain management 
● Impact of pain on a patient’s activities of daily living, quality of life and mental wellbeing; be able to offer some solutions for how to cope with these, including signposting to other agencies / members of the MDT. 
● Racial stereotyping in respect to pain management. 
"""
import re

def get_prompt_examples(target_subtopic,target_topic, json_filepath=MINERVA_FILE, min_examples=3):
    """Fetches up to 5 examples from the minerva bank for the given subtopic."""
    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            all_questions = json.load(f)
    except FileNotFoundError:
        return "Error: Could not find the Minerva JSON file. Proceeding without examples."
    except json.JSONDecodeError:
        return "Error: Minerva JSON file is invalid. Proceeding without examples."

    selected_questions = []
    seen_texts = set()

    # --- TIER 1: Exact Subtopic Match ---
    for q in all_questions:
        if q.get("subtopic") == target_subtopic:
            selected_questions.append(q)
            seen_texts.add(q["question"])
        if len(selected_questions) >= min_examples:
            break

    # --- TIER 2: Topic Match (if more needed) ---
    if len(selected_questions) < min_examples:
        for q in all_questions:
            # Check if topic matches and we haven't already added this question
            if q.get("topic") == target_topic and q["question"] not in seen_texts:
                selected_questions.append(q)
                seen_texts.add(q["question"])
            if len(selected_questions) >= min_examples:
                break

    # --- TIER 3: Start of File (if still more needed) ---
    if len(selected_questions) < min_examples:
        for q in all_questions:
            if q["question"] not in seen_texts:
                selected_questions.append(q)
                seen_texts.add(q["question"])
            if len(selected_questions) >= min_examples:
                break

    # 3. Format into a string for the prompt
    formatted_examples = ""
    for i, q in enumerate(selected_questions[:min_examples], 1): # Cap at min_examples to keep prompt size reasonable
        formatted_examples += f"Example {i}:\n"
        formatted_examples += f"Stem: {q['question']}\n"
        
        # Build options
        options_text = ""
        for letter, text in q.get('options', {}).items():
            options_text += f"{letter}: {text}\n"
            
        formatted_examples += f"Options:\n{options_text}"
        formatted_examples += f"Correct: {q['correct_answer']}\n"
        formatted_examples += f"Feedback: {q['feedback']}\n\n"

    return formatted_examples
# ── CANONICAL SUBTOPIC LIST ────────────────────────────────────────────────────
# <<< ADD THIS ENTIRE BLOCK
CANONICAL_SUBTOPICS = [
"Describe the nature of disease",
"Describe the process of acute inflammation",
"Describe the process of chronic inflammation",
"Describe the process of atherosclerosis formation",
"Describe the process of haemostasis",
"Describe the processes of apoptosis and necrosis",
"Describe the process of cell and tissue growth",
"Describe the process of carcinogenesis",
"Describe the processes of how cancer spreads within the body",
"Describe the process of tumour classification",
"Describe the fundamental aspects of cancer treatments",
"Describe the processes of tissue healing and repair",
"Describe the process of aging and the role of the autopsy in determining cause of death",
"List and describe the function of the main cellular and humoral components of the immune system",
"Explain the main features of innate and adaptive immunity, the key differences between them, and how they work together to create our immune system",
"Describe hypersensitivity and explain the key features of an allergic response",
"Explain how immunity changes with ageing and the impact of this on our susceptibility to disease",
"Describe the principles of immunotherapy in the management of cancer and inflammatory diseases",
"Describe the principles of immunisation and give examples of the different vaccines available and their benefits and drawbacks",
"Describe how immunological processes develop and become manifest and the consequences for the major organ systems detailed in Phase 2a",
"Describe the key features of pharmacodynamics of drug action (the biochemical and physiological effects of drugs)",
"Describe the key features of pharmacokinetics (the administration and subsequent fate of administered substances) and pharmacogenomics",
"Describe the mechanism of action and list examples of the following classes of drugs: Cholinergic, Adrenergic, Analgesics (opioids)",
"Define the following terms and explain their implications for prescribing and clinical management: Adverse drug reactions, Drug interactions",
"Describe the principles of drug discovery and development",
"Prescription Writing Early Years GP Prescribing Tasks",
"Describe the biology and classification of micro-organisms",
"Gram-positive pathogens",
"Gram-negative pathogens",
"Mycobacteria",
"Tuberculosis (TB)",
"Protozoa and Helminths",
"Immunisation and Notifiable Infectious Diseases (Cross Ref to Public Health)",
"Meningococcal infections: An important example of vaccine-preventable notifiable disease (Cross Ref to Public Health)",
"Viruses",
"Mycology and antifungals",
"Antivirals",
"Antibiotics",
"Healthcare-acquired infections",
"HIV Symposium",
"Full blood count",
"Anaemia",
"Haemoglobinopathies and red cell disorders",
"Bleeding disorders",
"Anticoagulation and thrombosis",
"Malignant haematology",
"Blood transfusion",
"Haematology emergencies",
"Apply theoretical frameworks of sociology to explain the varied responses of individuals, groups and societies to disease",
"Explain sociological factors that contribute to illness, the course of the disease and the success of treatment − including issues relating to health inequalities, the links between occupation and health and the effects of poverty and affluence",
"Explain and apply the basic principles of communicable disease control in hospital and community settings",
"Evaluate and apply epidemiological data in managing healthcare for the individual and the community",
"Critically appraise the results of relevant diagnostic, prognostic and treatment trials and other qualitative and quantitative studies as reported in the medical and scientific literature",
"Identify appropriate strategies for managing patients with dependence issues and other demonstrations of self-harm",
"Discuss psychological aspects of behavioural change and treatment compliance",
"Apply scientific method and approaches to medical research",
"Obstructive lung diseases",
"Restrictive lung diseases",
"Pleural disease",
"Lung cancer",
"Respiratory infections (overlap with microbiology/immunology/public health teaching)",
"Community acquired pneumonia",
"Influenza and pandemics",
"Occupational health and lung disorders",
"Palliative care in respiratory disease",
"Importance of MSK conditions",
"Fractures",
"Inherited / Autoimmune Connective tissue disorders",
"The inflamed joint and Gout",
"Spondyloarthropathy",
"Degenerative joint",
"Soft tissue MSK disorders",
"Osteoporosis & bone disorders",
"MSK infections",
"Back pain",
"Anatomy and Physiology",
"Appetite",
"Diabetes Mellitus – Part 1",
"Diabetes Mellitus – Part 2",
"Diabetes Mellitus – Part 3",
"Diabetes Mellitus – Part 4",
"Diabetes Mellitus – Part 5",
"Diabetes Mellitus – Part 6",
"Overview - Functional Anatomy and Physiology",
"Thyroid",
"Pituitary Hormones (Part 1; Anterior) - Regulation and Presentation of Pituitary Disease",
"Non-functioning tumours and pituitary hormone testing",
"Acromegaly and Prolactin",
"Pituitary Hormones – (Part 2; Posterior) - Water Balance, Hyponatraemia, Vasopressin Deficiency and Resistance (Diabetes Insipidus)",
"Circadian Rhythms, Adrenal Insufficiency and Cortisol Excess (Cushings syndrome)",
"Endocrine Hypertension",
"Parathyroid and Disorders of Calcium Metabolism",
"Puberty",
"Reproductive Endocrinology",
"Anticoagulants and Antiplatelets",
"Deep Vein Thrombosis (DVT) and Pulmonary Embolism (PE)",
"PVD",
"Atheroma",
"Chronic coronary syndrome",
"Acute coronary syndrome",
"ECG Parts 1 and 2",
"Inherited cardiac conditions",
"Cardiovascular Pharmacology Parts 1 and 2",
"Hypertension",
"Heart failure",
"Pericarditis",
"Valvular disease",
"Structural heart defects",
"Infective endocarditis",
"Clinically-Oriented Neuroanatomy",
"Dementia",
"Stroke",
"CNS Infections",
"Parkinsons disease and its differential diagnosis",
"Neurosurgery: An Introductory Lecture",
"Brain tumours",
"Neuro-rehabilitation",
"Consciousness: its assessment and common disorders",
"Cerebellar disease",
"Neuromuscular and muscular disorders",
"Multiple Sclerosis",
"Headaches",
"Spinal cord disorders",
"Epilepsy",
"Functional Neurological disorders (FND)",
"Motor Neurone Disease",
"Traumatic brain injury",
"Hyperkinetic Movement Disorders",
"Sensory symptoms",
"Review of Phase 1 kidney anatomy and renal physiology",
"Fluid balance",
"Penile cancer and Erectile dysfunction",
"Bladder Cancer",
"Kidney Cancer",
"Prostate Cancer, Prostate Specific Antigen (PSA) and Advanced Prostate Cancer",
"Testicular cancer",
"Systemic treatment of cancer",
"Chronic Kidney Disease (CKD)",
"Lower Urinary Tract Syndrome (LUTS)",
"Stone Disease and Obstruction",
"Mens Health",
"Glomerular disease",
"Acute Kidney Injury (AKI)",
"Urinary Tract Infection (UTI) and pyelonephritis",
"Reconstructive Urology",
"Liver disease",
"Hepatitis",
"Infection of the gastrointestinal and liver systems",
"Gastrointestinal bleeding",
"Pathology of gastrointestinal tumours",
"Gastrointestinal obstruction",
"Pathology of Gastritis, Malabsorption and Ulceration",
"Coeliac disease",
"Peptic ulcer disease",
"Gall stones",
"Inflammatory Bowel Disease (IBD)",
"Functional gut disorders",
"Peritonitis",
"Ascites",
"Polypharmacy and Holistic care",
"Child health surveillance and vaccinations",
"TB and Homeless health",
"Stroke",
"COPD",
"Diabetes",
"Palpitations",
"Dementia",
"Eating Disorders",
"Lower urinary tract symptoms",
"Liver disease, Hepatitis and Sexual health",
"ILA 11 - Pathology",
"ILA 12 - Immunology & Pharmacology",
"ILA 13 - Microbiology",
"ILA 14 - Endocrinology",
"ILA 15 - Cardiology & Neurology",
"ILA 16 - Renal & Urology",
]

def normalize(text: str) -> str:
    """Strip bullets, punctuation, extra spaces, and lowercase for fuzzy comparison."""
    text = re.sub(r'^[●•o\-\s]+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

_normalized_canonical = {normalize(s): s for s in CANONICAL_SUBTOPICS}

def validate_subtopics(extracted: list) -> list:
    """Return only extracted subtopics that match a canonical entry, using canonical spelling."""
    norm_keys = list(_normalized_canonical.keys())
    validated = []
    for subtopic in extracted:
        key = normalize(subtopic)
        matches = get_close_matches(key, norm_keys, n=1, cutoff=0.85)
        if matches:
            validated.append(_normalized_canonical[matches[0]])
        else:
            print(f"  [SKIPPED] No canonical match for: {subtopic!r}")
    return validated

BLOCK_HEADERS = {
    "pathology",
    "immunology",
    "pharmacology and prescribing",
    "microbiology",
    "haematology",
    "public health and population health science",
    "respiratory medicine",
    "musculoskeletal medicine msk",
    "diabetes mellitus and general endocrinology",
    "general endocrinology",
    "cardiovascular medicine",
    "neurology",
    "urology and renal medicine",
    "gastrointestinal and hepatic medicine",
    "teaching theme phase 2a early years gp eygp programme",
    "teaching theme phase 2a ila programme",
}

def extract_subtopics(syllabus: str) -> list:
    # 1. Clean lines
    lines = []
    for line in syllabus.splitlines():
        line = line.strip()
        if (not line
                or line in ["●", "o"]
                or line.startswith("Dr NR Chapman")
                or re.match(r"^Page \d+", line)):
            continue
        lines.append(line)

# 2. Merge continuation lines (non-bullet line following a non-terminated line)
    merged = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Absorb next line if current doesn't end a sentence, next isn't a bullet, 
        # AND next line doesn't start with a capital letter (which indicates a heading)
        while (i + 1 < len(lines)
               and not line.endswith((".", ":", "?", "!"))
               and not lines[i + 1].startswith("●")
               and not lines[i + 1].startswith("o ")
               and not re.match(r"^\d+\)", lines[i + 1])
               and not lines[i + 1][0].isupper()):  # <-- ADD THIS LINE
            i += 1
            line = line + " " + lines[i]
        merged.append(line)
        i += 1

    # 3. Extract subtopics using look-ahead:
    #    A line is a subtopic if it's not a bullet and the *next* line is a bullet
    subtopics = []
    for i, line in enumerate(merged):
        if line.startswith("●") or line.startswith("o "):
            continue
        if normalize(line) in BLOCK_HEADERS:
            continue
        # Look ahead: is the next non-empty line a bullet?
        for j in range(i + 1, min(i + 3, len(merged))):
            if merged[j].startswith("●") or merged[j].startswith("o "):
                subtopics.append(line)
                break

    return subtopics

# This will return clean, combined sentences like:
# ['Apply theoretical frameworks of sociology to explain the varied responses of individuals, groups and societies to disease.', 
#  'Explain sociological factors that contribute to illness, the course of the disease and the success of treatment − including issues relating to health inequalities...']


VALID_SUBTOPICS = validate_subtopics(extract_subtopics(SYLLABUS))

KNOWN_TOPICS = [
    "Introduction to Medicine and Medical Science (IMMS).", "Cardiovascular system.", "Respiratory system.", "Gastrointestinal tract and liver (GI-L).", "Neuroscience.", "Skin, UroGenital, Endocrine and Reproduction (SUGER).", "Musculoskeletal (MSK).", "Prescribing.", "Public health.", "Critical numbers.", "Early Years General Practice (EYGP)."
]

def get_syllabus_data(syllabus: str, valid_subtopics: list) -> dict:
    """Parses the syllabus and maps each valid subtopic to its specific topic and bullet points."""
    lines = []
    for line in syllabus.splitlines():
        line = line.strip()
        if (not line or line in ["●", "o"] or line.startswith("Dr NR Chapman") or re.match(r"^Page \d+", line)):
            continue
        lines.append(line)

    merged = []
    i = 0
    while i < len(lines):
        line = lines[i]
        while (i + 1 < len(lines) and not line.endswith((".", ":", "?", "!"))
               and not lines[i + 1].startswith("●") and not lines[i + 1].startswith("o ")
               and not re.match(r"^\d+\)", lines[i + 1]) and not lines[i + 1][0].isupper()):
            i += 1
            line += " " + lines[i]
        merged.append(line)
        i += 1

    data = {subtopic: {"topic": "General", "bullets": []} for subtopic in valid_subtopics}
    current_topic = "General"
    
    norm_valid = {normalize(s): s for s in valid_subtopics}
    norm_topics = {normalize(t): t for t in KNOWN_TOPICS}

    current_subtopic = None
    for line in merged:
        norm_line = normalize(line)
        if norm_line in norm_topics:
            current_topic = norm_topics[norm_line]
            current_subtopic = None
            continue
            
        if line.startswith("●") or line.startswith("o "):
            if current_subtopic:
                data[current_subtopic]["bullets"].append(line)
        else:
            if norm_line in norm_valid:
                current_subtopic = norm_valid[norm_line]
                data[current_subtopic]["topic"] = current_topic
            else:
                current_subtopic = None
    manual_topic_overrides = { 
        "Describe how immunological processes develop and become manifest and the consequences for the major organ systems detailed in Phase 2a": "Immunology"
    }
    for sub, correct_topic in manual_topic_overrides.items():
        if sub in data:
            data[sub]["topic"] = correct_topic

    return data

# Initialize the new data structure
SYLLABUS_DATA = get_syllabus_data(SYLLABUS, VALID_SUBTOPICS)
# ── PROMPTS ────────────────────────────────────────────────────────────────────
subtopics_for_prompt = '", "'.join(VALID_SUBTOPICS)

# ── PROMPTS ────────────────────────────────────────────────────────────────────
subtopics_for_prompt = '", "'.join(VALID_SUBTOPICS)

# 1. The base instructions (No examples)
BASE_SYSTEM_PROMPT = f"""
You are a medical examination question writer for a UK medical school.
Your sole purpose is to generate high-quality single best answer (SBA)
multiple choice questions for second year medical students.

RULES YOU MUST NEVER BREAK:
- Every question must follow the EXACT format shown in the examples below.
- MANDATORY QUESTION LEAD-IN: The 'stem' MUST end with a clear, explicit question.
- DIFFICULTY LEVEL: Target 2nd year UK medical students. Focus on the core, common conditions and mechanisms. Do not include post-graduate level minutiae, complex pharmacoloy, obscure drug dosing or advanced pathophysiology.
- Each question must have exactly 5 answer options labelled A through E.
- There is always exactly one correct answer. The other four are plausible
  distractors — wrong for a specific, clinically teachable reason.
- The clinical scenario must be realistic and internally consistent.
- Do not repeat questions from the examples provided.
- When asking about treatment focus on principles of management and full drug class names using generic terminology only. Strictly exclude trade names, niche medications, and their PK/PD, restricting pharmacological details to common, systems-based drugs.  
- When a question requires blood results, include reference ranges in brackets.
- You must return ONLY valid JSON. No preamble, no explanation, 
  no markdown code fences. Just the raw JSON array.
"""

# 2. The required JSON structure
JSON_OUTPUT_FORMAT = """
OUTPUT FORMAT — return exactly this JSON structure:
[
  {
    "topic": "Microbiology",
    "subtopic": "Tuberculosis (TB)",
    "question": "Stem text here...",
    "options": {
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "...",
      "E": "..."
    },
    "correct_answer": "B",
    "feedback": "B is correct because... A is incorrect because..."
  }
]
"""

def build_user_prompt(topic: str, subtopic: str, bullets: list, num_questions: int) -> str:
    bullet_text = "\n".join(bullets) if bullets else "No specific objectives provided."
    return f"""Generate exactly {num_questions} SBA questions on the subtopic: {subtopic}

SYLLABUS OBJECTIVES FOR THIS SUBTOPIC:
{bullet_text}

Requirements:
- All {num_questions} questions must test different learning objectives from the syllabus objectives above.
- Vary the clinical setting (e.g. GP, ED, ward, clinic)
- Vary what is being asked (e.g. diagnosis, investigation, management, mechanism)
- The "topic" field must be exactly: "{topic}"
- The "subtopic" field must be exactly: "{subtopic}"
- Return exactly {num_questions} questions in the JSON array format. Nothing else."""


# ── CORE FUNCTIONS ─────────────────────────────────────────────────────────────

def load_existing_bank(filepath: str) -> list:
    """Load existing questions from the JSON file, or return empty list."""
    if os.path.exists(filepath):
        try:
            # Check if file is empty
            if os.path.getsize(filepath) == 0:
                return []
                
            with open(filepath, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            # If the file is corrupted or not valid JSON, return empty list
            print(f"Note: {filepath} was empty or corrupted. Starting a fresh bank.")
            return []
    return []

def _next_card_id(bank: list) -> int:
    """
    Scan the bank for existing card IDs and return the next integer to use.
    Returns 1 if no IDs are present yet (fresh bank).
    """
    max_id = 0
    for item in bank:
        raw = item.get("id", "")
        if isinstance(raw, str) and raw.startswith("card_"):
            try:
                num = int(raw[5:])   # strip "card_" prefix
                if num > max_id:
                    max_id = num
            except ValueError:
                pass
    return max_id + 1


# ── Column order to match your Supabase table ───────────────────────────────────────
CSV_COLUMNS = [
    "id",
    "topic",
    "subtopic",
    "question",
    "options",          # stored as JSONB in Supabase → serialised as JSON string
    "correct_answer",
    "feedback",
    "generated_at",
]


def _bank_to_csv(bank: list, csv_path: str) -> None:
    """Write the question bank to a CSV file ready for Supabase upload."""
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=CSV_COLUMNS,
            extrasaction="ignore",   # silently drop any extra JSON keys
            quoting=csv.QUOTE_ALL,   # quote every field → safest for Supabase
        )
        writer.writeheader()
        for row in bank:
            if "options" in row and isinstance(row["options"], dict):
                row = dict(row)      # don't mutate the original
                row["options"] = json.dumps(row["options"], ensure_ascii=False)
            writer.writerow(row)
    print(f"  [csv]    Exported {len(bank)} record(s)  →  {csv_path}")


def save_bank(filepath: str, bank: list):
    """
    Save the question bank with four automatic steps:

    1. FILTER     – removes any entry whose 'question' field does not end with '?'
    2. ID STAMP   – assigns a unique card ID to every entry that lacks one,
                    resuming from the highest existing ID (or card_0001 if fresh).
    3. JSON SAVE  – writes the cleaned bank back to the JSON file.
    4. CSV EXPORT – writes a Supabase-ready CSV alongside the JSON file
                    with the same base name (e.g. question_bank.csv).
    """
    # ── Step 1: filter non-questions ────────────────────────────────────────
    before = len(bank)
    bank = [
        item for item in bank
        if item.get("question", "").strip().endswith("?")
    ]
    removed = before - len(bank)
    if removed:
        print(f"  [filter] Removed {removed} non-question item(s) before saving.")

    # ── Step 2: assign IDs to any entry that lacks one ─────────────────
    next_id = _next_card_id(bank)
    stamped = 0
    for item in bank:
        if not item.get("id"):
            item["id"] = f"card_{next_id:04d}"
            next_id += 1
            stamped += 1
    if stamped:
        print(f"  [ids]    Stamped {stamped} new card ID(s). Next available: card_{next_id:04d}.")

    # ── Step 3: write JSON to disk ──────────────────────────────────────
    with open(filepath, "w") as f:
        json.dump(bank, f, indent=2)

    # ── Step 4: export CSV alongside the JSON ──────────────────────────────
    csv_path = os.path.splitext(filepath)[0] + ".csv"
    _bank_to_csv(bank, csv_path)

def generate_questions(topic: str, subtopic: str, bullets: list, num_questions: int, model_name: str, is_first_call: bool = False) -> list:
    """Send the prompt to Gemini and return parsed questions."""
    client = genai.Client(api_key=API_KEYS[current_key_idx])
    
    user_prompt = build_user_prompt(topic, subtopic, bullets, num_questions)
    
    # Fetch dynamic examples and build the final system prompt
    examples_text = get_prompt_examples(subtopic, topic)
    dynamic_system_prompt = (
        BASE_SYSTEM_PROMPT + 
        "\nEXEMPLAR QUESTIONS (learn format, tone, stem length, distractor style):\n\n" + 
        examples_text + 
        JSON_OUTPUT_FORMAT
    )
    
    if is_first_call:
        print("\n" + "="*80)
        print("🔍 DEBUG: FIRST API CALL PAYLOAD")
        print("="*80)
        print(f"MODEL: {model_name}")
        print("-" * 80)
        print("SYSTEM INSTRUCTION:")
        print(dynamic_system_prompt)
        print("-" * 80)
        print("USER PROMPT:")
        print(user_prompt)
        print("="*80 + "\n")

    response = client.models.generate_content(
        model=model_name,
        contents=user_prompt,
        config={
            "system_instruction": dynamic_system_prompt,
            "response_mime_type": "application/json" 
        }
    )
    
    raw = response.text.strip()
    clean_json = re.sub(r'^```json|```$', '', raw, flags=re.MULTILINE).strip()

    try:
        questions = json.loads(clean_json)
        for q in questions:
            q["generated_at"] = datetime.now().isoformat()
            if "subtopic" not in q:
                q["subtopic"] = subtopic
            if "topic" not in q or q["topic"] == "Neurology": # Failsafe just in case
                q["topic"] = topic

        return questions
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON for {subtopic}: {e}")
        return []

def display_questions(questions: list):
    """Print questions to screen in a readable format."""
    if not questions:
        print("No questions to display.")
        return

    for i, q in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"Question {i} | {q.get('subtopic', 'General')}")
        print(f"{'='*60}")
        print(f"\n{q['question']}\n")
        
        for letter, option in q['options'].items():
            print(f"  {letter}. {option}")
            
        print(f"\nCorrect answer: {q['correct_answer']}")
        print(f"Feedback: {q['feedback']}")



# ── MAIN ───────────────────────────────────────────────────────────────────────
def get_seconds_until_1am() -> float:
    """Calculates the exact number of seconds from now until the next 1:00 AM."""
    now = datetime.now()
    # Create a target time for 1:00 AM today
    target = now.replace(hour=1, minute=0, second=0, microsecond=0)
    
    # If it's already past 1:00 AM today, target 1:00 AM tomorrow
    if now >= target:
        target += timedelta(days=1)
        
    return (target - now).total_seconds()

def show_bank_summary(bank: list):
    """Show how many questions exist per subtopic."""
    counts = {}
    for q in bank:
        subtopic = q.get("subtopic", "Unknown")
        counts[subtopic] = counts.get(subtopic, 0) + 1
    
    print("\nCurrent bank coverage:")
    for subtopic in VALID_SUBTOPICS:
        count = counts.get(subtopic, 0)
        bar = "█" * count
        print(f"  {subtopic:<50} {bar} {count}")
    print()
    
def main():
    print("Starting automated question generation loop...")
    global current_key_idx
    # Load the bank once at the start
    bank = load_existing_bank(OUTPUT_FILE)
    
# 1. SHOW THE FULL SUMMARY DASHBOARD AT STARTUP
    if bank:
        show_bank_summary(bank)
    else:
        print("\nBank is currently empty. Starting fresh!")

    # Find where to resume by picking the subtopic with the fewest questions
    counts = {sub: 0 for sub in VALID_SUBTOPICS}
    for q in bank:
        sub = q.get("subtopic", "Unknown")
        if sub in counts:
            counts[sub] += 1
            
    # Get the subtopic name with the minimum count, then find its index
    starting_subtopic = min(counts, key=counts.get)
    subtopic_idx = VALID_SUBTOPICS.index(starting_subtopic)
    
    print(f"\nResuming script at: '{starting_subtopic}' (Currently has {counts[starting_subtopic]} questions)")
    models = ["gemini-3-flash-preview", "gemini-2.5-flash"]
    current_model_idx = 0
    
    HIGH_YIELD_TOPICS = {
        "Microbiology",
        "Respiratory Medicine",
        "Cardiovascular Medicine",
        "Gastrointestinal and Hepatic Medicine",
        "Neurology",
        "Pharmacology and Prescribing"
    }
    first_run = True

    while True:
        current_model = models[current_model_idx]
        subtopic = VALID_SUBTOPICS[subtopic_idx]
        
        # Grab the specific topic and bullets for this subtopic
        topic = SYLLABUS_DATA[subtopic]["topic"]
        bullets = SYLLABUS_DATA[subtopic]["bullets"]
        
        # Determine how many questions to generate
        num_questions = 2 if topic in HIGH_YIELD_TOPICS else 1
        
        # Calculate current questions for this specific subtopic
        current_count = sum(1 for q in bank if q.get("subtopic", "") == subtopic)
        
        print(f"\n" + "="*60)
        print(f"🎯 TOPIC: {topic} | SUBTOPIC: {subtopic}")
        print(f"\nGenerating {num_questions} questions on: {subtopic}")
        print(f"Using model: {current_model}")
        print("="*60)
        
        try:
            questions = generate_questions(
                topic=topic,
                subtopic=subtopic, 
                bullets=bullets, 
                num_questions=num_questions,
                model_name=current_model, 
                is_first_call=first_run 
            )

            first_run = False

            if questions:
                display_questions(questions)
                bank.extend(questions)
                save_bank(OUTPUT_FILE, bank)

                new_count = current_count + len(questions)
                print(f"✓ Added {len(questions)} questions. Total for '{subtopic}' is now {new_count}. Total in bank: {len(bank)}")
            else:
                print("No questions generated this round (possible JSON error).")
                
            # SUCCESS: Move to the next subtopic
            subtopic_idx = (subtopic_idx + 1) % len(VALID_SUBTOPICS)
            
            # Brief pause to avoid hammering the API
            print("Sleeping for 60 seconds before the next request...")
            time.sleep(60)
            
        except Exception as e:
            first_run = False
            error_msg = str(e).lower()
            print(f"\nAPI error: {e}")
            
            # Check if the error is due to hitting the quota/exhaustion
            if "exhausted" in error_msg or "quota" in error_msg or "429" in error_msg:
                print(f"Key {current_key_idx + 1} exhausted.")
                
                # Move to the next key
                current_key_idx += 1
                
                # Check if ALL keys are exhausted
                if current_key_idx >= len(API_KEYS):
                    print("All API keys exhausted for current model.")
                    
                    # Try switching to the next model and reset keys to the start
                    current_model_idx += 1
                    current_key_idx = 0 
                    
                    # If we've run out of models AND keys
                    if current_model_idx >= len(models):
                        sleep_seconds = get_seconds_until_1am()
                        resume_time = datetime.now() + timedelta(seconds=sleep_seconds)
                        
                        print(f"Everything exhausted. Sleeping until 1AM: {resume_time}")
                        time.sleep(sleep_seconds)
                        
                        # RESET EVERYTHING AT 1AM
                        current_model_idx = 0
                        current_key_idx = 0
                else:
                    print(f"Switching to next API key (Index {current_key_idx})...")
            else:
                print("Standard error, retrying in 60s...")
                time.sleep(60)
            continue

if __name__ == "__main__":
    main()