import streamlit as st
import os
import json
import warnings
import datetime
from document_intelligence import validate_document,extract_entities,extract_text_from_pdf

# Optionally ignore warnings
warnings.filterwarnings("ignore")

# Set page configuration to wide
st.set_page_config(layout="wide")

# Custom CSS to adjust the width of elements, align labels, and style buttons
st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        max-width: 100%;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    .custom-button {
        background-color: #4CAF50;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border: none;
        border-radius: 12px;
    }
    .custom-button:hover {
        background-color: #45a049;
    }
    .center-align {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Center the main header using HTML and Markdown
# st.markdown(
#     """
#     <h1 style='text-align: center;'>Oorwin Document Validator</h1>
#     """, 
#     unsafe_allow_html=True
# )
# Title for the document validation section
st.subheader('Document Validation')

temp_dir = "temp_dir"
# Export License Template section
st.markdown('<div class="center-align">', unsafe_allow_html=True)

col1, col2 , col3 = st.columns([2, 3, 2])
with col1:
    st.write("") 
    st.write("") 
    st.markdown("**Export License Template**")

with col2:
    template_file = st.file_uploader('', key='template_file')
st.markdown('</div>', unsafe_allow_html=True)


temp_template_file=""
if template_file is not None:
    # Save the uploaded file to a temporary location
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_template_file = os.path.join(temp_dir, f"{timestamp}_{template_file.name}")
    with open(temp_template_file, "wb") as f:
        f.write(template_file.getbuffer())
        # st.write(temp_template_file)
        

# Export License Document section
st.markdown('<div class="center-align">', unsafe_allow_html=True)

col1, col2 , col3 = st.columns([2, 3, 2])
with col1:
    st.write("") 
    st.write("") 
    st.markdown("**Export License Document**")

with col2:
    input_file = st.file_uploader('', key='input_file')
st.markdown('</div>', unsafe_allow_html=True)


temp_input_file=""
if input_file is not None:
    # Save the uploaded file to a temporary location
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_input_file = os.path.join(temp_dir, f"{timestamp}_{input_file.name}")
    with open(temp_input_file, "wb") as f:
        f.write(input_file.getbuffer())



# Centered Validate button
col_center4, col_center5, col_center6 = st.columns([3, 1, 3])
with col_center5:
    if st.button('Validate Document'):
        if temp_template_file and temp_input_file:
            # st.write('Document validated')
            text=validate_document(temp_template_file,temp_input_file)
            st.success(text)
            # st.success("Testing: Document is compatible")
        else:
            st.error('Please upload both the template file and the input file.')
        
# ===================================================================================
# File Validation Code Start Here
# ===================================================================================
# Separation line
st.markdown('---')

# Title for the document verification section
st.subheader('Document Verification')

# Export License Document verification section
col1, col2 , col3 = st.columns([2, 3, 2])
with col1:
    st.write("") 
    st.write("") 
    st.markdown("**Export License Document**")

with col2:
    verify_document_file = st.file_uploader('', key='verify_document_file')
st.markdown('</div>', unsafe_allow_html=True)


temp_verify_document_file=""
if verify_document_file is not None:
    # Save the uploaded file to a temporary location
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_verify_document_file = os.path.join(temp_dir, f"{timestamp}_{verify_document_file.name}")
    with open(temp_verify_document_file, "wb") as f:
        f.write(verify_document_file.getbuffer())

# Centered Validate button
col_center7, col_center8, col_center9 = st.columns([3, 1, 3])
export_authorisation_no = ""
exporter_address = ""
isInformationMissing=False
isVerifyCommandExecuted=False
isAddressMissing = False
isNumberMissing = False
with col_center8:
    if st.button('Verify Document'):
        isVerifyCommandExecuted=True
        # st.write('Verification Document validated')
        text = extract_text_from_pdf(temp_verify_document_file)
        #Test Comment
        #Valid Case-Both are there
        # text="""GOVERNMENT OF INDIA MINISTRY OF FINANCE (Department of Revenue) Central Bureau of Narcotics ORIGINAL - EXPORTER'S COPY (TO ACCOMPANY THE CONSIGNMENT) S. NO0033396 सत्यमेव जयते Authorisation for Official Approval of Export (The Narcotic Drugs and Psychotropic Substances Rules, 1985) Authorisation is not valid unless it bears official seal of the Issuing Authority hereon Export Authorisation No .: P-EXP-10283/2021 F.No.XVI/4/5589/Tech/Psy/2020 NARCOTICS COMMISSIONER being the authority empowered to issue export authorisation under the Narcotic Drugs and Psychotropic Substances Rules, 1985 hereby authorises and permits the following exportation of Psychotropic Substances from India Exporter: Umedica Laboratories Pvt. Ltd., Plot No. 221 G.I.D.C., Vapi-396 195 Gujarat- India Consignee: Pharma Care International Pvt Ltd. Kathmandu-10, Baneshwor, Nepal, Port of Export: Raxaul, India Port of Entry: Kathmandu, Nepal via Birgunj Psychotropic Substances to be exported: Item No. Number of Packages Name of the substance / preparation Basic substance/ content 01 154 Corrougated Shipper 2,30,000 Ampoules of Tramadol Hcl Injection, 50mg/ml, (Utram) = 11.50 Kg Tramadol HCL Tramadol 10.12 Kg The exportation to be made in one consignment from the designated port of exporton or before the 215' day of April, 2021 The importation of these drugs into the country of destination has been authorised by official Import Permission No.230 dated 03.11.2020 issued by the Ministry of Home Affairs Narcotics Drugs Control Section, Nepal. Date of Issue:21.01.2021 Place of Issue: Gwalior (Arvind Saxena) Haxeno Superintendent (Technical) Authorised Signatory Name and Designation of the Authorised Officer Designation and Address of the Issuing Authority Narcotics Commissioner Central Bureau of Narcotics, 19. The Mall, Morar, Gwalior-474006 Madhya Pradesh, INDIA Form No.5(Rule 58) भारतसरकार वित मंत्रालय केन्द्रीय नारकोटिक्सब्यूरो 19, मालरोड, मुरार, ग्वालियर- 474006 सत्यमेव जयते (PBX) : (91) 751-2368996/ 2368997; FAX: (91) 751-2368111/; GRAM: NARCOM; E-MAIL: supdt-tech@cbn.nic.in Government of India Ministry of Finance Central Bureau of Narcotics 19,The Mall, Morar, Gwalior (M.P.) - 474006 F. No. XVI/4/5589/T/P/2020 1158 To, Umedica Laboratories Pvt. Ltd., Plot No. 221 G.I.D.C., Vapi-396 195 Gujarat Dated, the January, 2021 25 प्रिय महोदय / महोदयाDear Madam/Sir, faw Subject: Export of Psychotropic Substances vide Export Authorizations No. P- EXP-10283/2021 dated 21.01.2021. कृपया इसके साथ संलग्न उपरोक्त निर्यात प्राधिकरण प्राप्त करें। Enclosed please find herewith aforesaid Export Authorizations. आपको अगले पृष्ठ में दिये गये अनुदेशों के अनुसार निर्यात का प्रमाण प्रस्तुत करने का आदेश दिया जाता है।You are hereby directed to submit the proof of export as per the instructions given overleaf. कृपया सुनिश्चित करें कि निम्न रेखांकित अनुदेशों का कठोरता से अनुपालन किया जाता है। Please ensure that underlying instructions are strictly complied with. ऐसा करने में असफल होने का परिणाम होगा कि भविष्य में मन:प्रभावी पदार्थों के निर्यात हेतु आवेदनों के विरूद्ध निर्यात प्राधिकरण जारी नहीं होगा ।Failure to do so will result in non- issuance of Export Authorization against future application for exportof psychotropic substances. Encl. As above. Copy to : भवदीय, Yours sincerely, Havere (Arvind Saxena) अधीक्षक (तकनीकी) / Superintendent (Technical) (i) The Asstt. Commissioner Land Customs Station, Raxaul Distt. - East Champaran- 845305, India along with Duplicate copy with the request to return the same indicating the date of export and the quantity of substance exported in order to enable us to fulfill the international obligation in time. (ii) Joint Secretary Chief Narcotics Control Officers Planning and Special Service Division Ministry of Home Affairs Singh Durbar Kathmandu, Nepal, along with Triplicate copy with the request to return the same to this office duly endorsed in accordance with the provisions of Article 16 of the UN Convention on Psychotropic Substances, 1971 specifying the quantity actual imported. (iii) The Commissioner, Food and Drug Administration, Gujarat State, Block No: 8, 1st Floor, Dr. Jivraj Mehta Bhawan, Gandhinagar along with Quadruplicate copy for records. अधीक्षक (तकनीकी) /Superintendent (Technical) 1 PTO :selected: :selected: :selected: :unselected:"""
        
        #InValid Case-Address Missing
        # text =""""सत्यमेव जयते\nGOVERNMENT OF INDIA MINISTRY OF FINANCE (Department of Revenue) Central Bureau of Narcotics\nS. NO0033396\nORIGINAL - EXPORTER'S COPY (TO ACCOMPANY THE CONSIGNMENT)\nAuthorisation for Official Approval of Export (The Narcotic Drugs and Psychotropic Substances Rules, 1985)\nAuthorisation is not valid unless it bears official seal of the Issuing Authority hereon\nExport Authorisation No .: P-EXP-10283/2021\nF.No.XVI/4/5589/Tech/Psy/2020\nNARCOTICS COMMISSIONER being the authority empowered to issue export authorisation under the Narcotic Drugs and Psychotropic Substances Rules, 1985 hereby authorises and permits the following exportation of Psychotropic Substances from India\nExporter:\nConsignee:\nPort of Export:\nRaxaul, India\nPort of Entry:\nKathmandu, Nepal via Birgunj\nPsychotropic Substances to be exported:\nItem No.\nNumber of Packages\nName of the substance / preparation\nBasic substance/ content\n01\n154 Corrougated Shipper\n2,30,000 Ampoules of Tramadol Hcl Injection, 50mg/ml, (Utram) = 11.50 Kg Tramadol HCL\nTramadol 10.12 Kg\nThe exportation to be made in one consignment from the designated port of exporton or before the 215' day of April, 2021\nThe importation of these drugs into the country of destination has been authorised by official Import Permission No.230 dated 03.11.2020 issued by the Ministry of Home Affairs Narcotics Drugs Control Section, Nepal.\nDate of Issue:21.01.2021\nPlace of Issue: Gwalior\n(Arvind Saxena)\nHaxeno\nSuperintendent (Technical)\nAuthorised Signatory\nName and Designation of the Authorised Officer\nDesignation and Address of the Issuing Authority Narcotics Commissioner Central Bureau of Narcotics, 19. The Mall, Morar, Gwalior-474006 Madhya Pradesh, INDIA\nForm No.5(Rule 58)\nभारतसरकार वित मंत्रालय केन्द्रीय नारकोटिक्सब्यूरो 19, मालरोड, मुरार, ग्वालियर- 474006 सत्यमेव जयते\nGovernment of India Ministry of Finance Central Bureau of Narcotics 19,The Mall, Morar, Gwalior (M.P.) - 474006\n(PBX) : (91) 751-2368996/ 2368997; FAX: (91) 751-2368111/; GRAM: NARCOM; E-MAIL: supdt-tech@cbn.nic.in\nF. No. XVI/4/5589/T/P/2020\n1158\nDated, the\n25\nJanuary, 2021\nTo,\nप्रिय महोदय / महोदयाDear Madam/Sir,\nfaw Subject: Export of Psychotropic Substances vide Export Authorizations No. P- EXP-10283/2021 dated 21.01.2021\nकृपया इसके साथ संलग्न उपरोक्त निर्यात प्राधिकरण प्राप्त करें। Enclosed please find herewith aforesaid Export Authorizations.\nआपको अगले पृष्ठ में दिये गये अनुदेशों के अनुसार निर्यात का प्रमाण प्रस्तुत करने का आदेश दिया जाता है।You are hereby directed to submit the proof of export as per the instructions given overleaf.\nकृपया सुनिश्चित करें कि निम्न रेखांकित अनुदेशों का कठोरता से अनुपालन किया जाता है। Please ensure that underlying instructions are strictly complied with. ऐसा करने में असफल होने का परिणाम होगा कि भविष्य में मन:प्रभावी पदार्थों के निर्यात हेतु आवेदनों के विरूद्ध निर्यात प्राधिकरण जारी नहीं होगा ।Failure to do so will result in non- issuance of Export Authorization against future application for exportof psychotropic substances.\nEncl. As above.\nCopy to :\nभवदीय, Yours sincerely,\nHavere\n(Arvind Saxena)\nअधीक्षक (तकनीकी) / Superintendent (Technical)\n(i) The Asstt. Commissioner Land Customs Station, Raxaul Distt. - East Champaran- 845305, India along with Duplicate copy with the request to return the same indicating the date of export and the quantity of substance exported in order to enable us to fulfill the international obligation in time.\n(ii) Joint Secretary Chief Narcotics Control Officers Planning and Special Service Division Ministry of Home Affairs Singh Durbar Kathmandu, Nepal, along with Triplicate copy with the request to return the same to this office duly endorsed in accordance with the provisions of Article 16 of the UN Convention on Psychotropic Substances, 1971 specifying the quantity actual imported. (iii) The Commissioner, Food and Drug Administration, Gujarat State, Block No: 8, 1st Floor, Dr. Jivraj Mehta Bhawan, Gandhinagar along with Quadruplicate copy for records.\n1\nअधीक्षक (तकनीकी) /Superintendent (Technical)\nPTO :selected:"""
        
        #InValid Case-Export_Authorisation_No missing
        # text ="""GOVERNMENT OF INDIA MINISTRY OF FINANCE (Department of Revenue) Central Bureau of Narcotics\nORIGINAL - EXPORTER'S COPY (TO ACCOMPANY THE CONSIGNMENT)\nS. NO0033396\nसत्यमेव जयते\nAuthorisation for Official Approval of Export (The Narcotic Drugs and Psychotropic Substances Rules, 1985)\nAuthorisation is not valid unless it bears official seal of the Issuing Authority hereon\nExport Authorisation No.\nF.No.XVI/4/5589/Tech/Psy/2020\nNARCOTICS COMMISSIONER being the authority empowered to issue export authorisation under the Narcotic Drugs and Psychotropic Substances Rules, 1985 hereby authorises and permits the following exportation of Psychotropic Substances from India\nExporter:\nUmedica Laboratories Pvt. Ltd.,\nPlot No. 221 G.I.D.C., Vapi-396 195\nGujarat- India\nConsignee:\nPharma Care International Pvt Ltd.\nKathmandu-10, Baneshwor, Nepal,\nPort of Export:\nRaxaul, India\n"""
        
        #InValid Case-Both Fields missing
        # text =""" सत्यमेव जयते\nGOVERNMENT OF INDIA MINISTRY OF FINANCE (Department of Revenue) Central Bureau of Narcotics\nS. NO0033396\nORIGINAL - EXPORTER'S COPY (TO ACCOMPANY THE CONSIGNMENT)\nAuthorisation for Official Approval of Export (The Narcotic Drugs and Psychotropic Substances Rules, 1985)\nAuthorisation is not valid unless it bears official seal of the Issuing Authority hereon\nExport Authorisation No\nF.No.XVI/4/5589/Tech/Psy/2020\nNARCOTICS COMMISSIONER being the authority empowered to issue export authorisation under the Narcotic Drugs and Psychotropic Substances Rules, 1985 hereby authorises and permits the following exportation of Psychotropic Substances from India\nExporter:\nConsignee:\nPharma Care International Pvt Ltd.\nKathmandu-10, Baneshwor, Nepal,\nPort of Export:\nRaxaul, India\nPort of Entry:\nKathmandu, Nepal via Birgunj\nPsychotropic Substances to be exported:\nItem No.\nNumber of Packages\nName of the substance / preparation\nBasic substance/ content\n01\n154 Corrougated Shipper\n2,30,000 Ampoules of Tramadol Hcl Injection, 50mg/ml, (Utram) = 11.50 Kg Tramadol HCL\nTramadol 10.12 Kg\nThe exportation to be made in one consignment from the designated port of exporton or before the 215' day of April, 2021\nThe importation of these drugs into the country of destination has been authorised by official Import Permission No.230 dated 03.11.2020 issued by the Ministry of Home Affairs Narcotics Drugs Control Section, Nepal.\nDate of Issue:21.01.2021\nPlace of Issue: Gwalior\n(Arvind Saxena)\nHaxeno\nSuperintendent (Technical)\nAuthorised Signatory\nName and Designation of the Authorised Officer\nDesignation and Address of the Issuing Authority Narcotics Commissioner Central Bureau of Narcotics, 19. The Mall, Morar, Gwalior-474006 Madhya Pradesh, INDIA\nForm No.5(Rule 58)\nभारतसरकार वित मंत्रालय केन्द्रीय नारकोटिक्सब्यूरो 19, मालरोड, मुरार, ग्वालियर- 474006 सत्यमेव जयते\nGovernment of India Ministry of Finance Central Bureau of Narcotics 19,The Mall, Morar, Gwalior (M.P.) - 474006\n(PBX) : (91) 751-2368996/ 2368997; FAX: (91) 751-2368111/; GRAM: NARCOM; E-MAIL: supdt-tech@cbn.nic.in\nF. No. XVI/4/5589/T/P/2020\n1158\nDated, the\n25\nJanuary, 2021\nTo,\nप्रिय महोदय / महोदयाDear Madam/Sir,\nfaw Subject: Export of Psychotropic Substances vide Export Authorizations No. P- EXP-10283/2021 dated 21.01.2021\nकृपया इसके साथ संलग्न उपरोक्त निर्यात प्राधिकरण प्राप्त करें। Enclosed please find herewith aforesaid Export Authorizations.\nआपको अगले पृष्ठ में दिये गये अनुदेशों के अनुसार निर्यात का प्रमाण प्रस्तुत करने का आदेश दिया जाता है।You are hereby directed to submit the proof of export as per the instructions given overleaf.\nकृपया सुनिश्चित करें कि निम्न रेखांकित अनुदेशों का कठोरता से अनुपालन किया जाता है। Please ensure that underlying instructions are strictly complied with. ऐसा करने में असफल होने का परिणाम होगा कि भविष्य में मन:प्रभावी पदार्थों के निर्यात हेतु आवेदनों के विरूद्ध निर्यात प्राधिकरण जारी नहीं होगा ।Failure to do so will result in non- issuance of Export Authorization against future application for exportof psychotropic substances.\nEncl. As above.\nCopy to :\nभवदीय, Yours sincerely,\nHavere\n(Arvind Saxena)\nअधीक्षक (तकनीकी) / Superintendent (Technical)\n(i) The Asstt. Commissioner Land Customs Station, Raxaul Distt. - East Champaran- 845305, India along with Duplicate copy with the request to return the same indicating the date of export and the quantity of substance exported in order to enable us to fulfill the international obligation in time.\n(ii) Joint Secretary Chief Narcotics Control Officers Planning and Special Service Division Ministry of Home Affairs Singh Durbar Kathmandu, Nepal, along with Triplicate copy with the request to return the same to this office duly endorsed in accordance with the provisions of Article 16 of the UN Convention on Psychotropic Substances, 1971 specifying the quantity actual imported. (iii) The Commissioner, Food and Drug Administration, Gujarat State, Block No: 8, 1st Floor, Dr. Jivraj Mehta Bhawan, Gandhinagar along with Quadruplicate copy for records.\n1\nअधीक्षक (तकनीकी) /Superintendent (Technical)\nPTO :selected:"""

        # st.write(text)
        entities=extract_entities(text)
        # entities=""" {\n    
        #  "Export_Authorisation_No": "P-EXP-10283/2021",\n   
        #  "Exporter_Address": "Umedica Laboratories Pvt. Ltd., Plot No. 221 G.I.D.C., Vapi-396 195 Gujarat- India"\n
        #  }"""
        
        
        # Extract variables
        export_authorisation_no = entities["Export_Authorisation_No"]
        exporter_address = entities["Exporter_Address"]
        isNumberMissing = not bool(export_authorisation_no)
        isAddressMissing = not bool(exporter_address)
        isInformationMissing = isNumberMissing or isAddressMissing

# Print extracted variables
if isVerifyCommandExecuted and not isInformationMissing:
    col1, col2 = st.columns([9, 1])
    with col1:
        st.markdown(f"**Export Authorization Number:** {export_authorisation_no}")

    col3, col4 = st.columns([9, 1])
    with col3:
        st.markdown(f"**Exporter Address:** {exporter_address}")
elif isVerifyCommandExecuted and isInformationMissing:
    st.markdown('### Information Missing')
    missing_info = []
    if isNumberMissing:
        missing_info.append('- Export Authorization Number')
    if isAddressMissing:
        missing_info.append('- Exporter Address')
    st.error('\n'.join(missing_info))
